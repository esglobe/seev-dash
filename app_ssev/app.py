import os
import dash
from dash import Dash, html, dcc
import plotly.express as px
from flask import Flask

debug = True
port = os.environ["PORT"]

# Server/app
server = Flask(__name__)
app = Dash(__name__,
          server=server,
          meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
          use_pages=True
          )

app.layout = html.Div([



	html.H1('Multi-page app with Dash Pages'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])

#https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-brain-viewer/app.py
# app.layout = html.Div(
#     [
#         html.Div(
#             [
#                 html.Div(
#                     [
#                         html.Div(
#                             [
#                                 html.Div(
#                                     [
#                                         html.H1('div 1')
#                                     ],
#                                     className="header__title",
#                                 ),
#                                 html.Div(
#                                     [
#                                         html.H1('div 2')
#                                     ],
#                                     className="header__info pb-20",
#                                 ),
#                                 html.Div(
#                                     [
#                                         html.H1('div 3')
#                                     ],
#                                     className="header__button",
#                                 ),
#                             ],
#                             className="header pb-20",
#                         ),
#                         html.Div(
#                             [
#                                 html.H1('div 4')
#                             ],
#                             className="graph__container",
#                         ),
#                     ],
#                     className="container",
#                 )
#             ],
#             className="two-thirds column app__left__section",
#         ),
#         html.Div(
#             [
#                 html.Div(
#                     [
#                         html.Div(
#                             [
#                                 html.H1('div 5')
#                             ]
#                         )
#                     ],
#                     className="colorscale pb-20",
#                 ),
#                 html.Div(
#                     [
#                         html.H1('div 6')
#                     ],
#                     className="pb-20",
#                 ),
#                 html.Div(
#                     [
#                         html.H1('div 7')
#                     ],
#                     className="pb-20",
#                 ),
#                 html.Div(
#                     [
#                         html.H1('div 8')
#                     ],
#                     className="pb-20",
#                 ),
#                 html.Div(
#                     [
#                         html.H1('div 9'),
#                         dash.page_container
#                     ]
#                 ),
#             ],
#             className="one-third column app__right__section",
#         ),
#         dcc.Store(id="annotation_storage"),
#     ]
# )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=port, debug=debug)
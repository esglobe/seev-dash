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
          use_pages=True
          )
          
app.title = 'SSEV'

#------------------------------
app.layout = html.Div([

    #--
    html.Div([
        html.A(href=dash.page_registry['pages.home']["relative_path"],
                children=[
                    html.Img(src=app.get_asset_url("ssev-logo.png"),
                             className="imag__header__title")
                    ]
        )
        ],className="header__title"),
        
    #--
    html.Div([
        html.H2('SSEV'),
        html.H3('Sistema para el Seguimiento de Ecosistemas Venezolanos'),
        html.Br()
        ],className="header__info"),

    #--
    html.Div([
        html.H4('Contenido:'),
        html.Div([
                html.Div([dcc.Link(f"{dash.page_registry['pages.home']['name']}",
                                href=dash.page_registry['pages.home']["relative_path"])]),
                html.Div([dcc.Link(f"{dash.page_registry['pages.temperatura']['name']}",
                                href=dash.page_registry['pages.temperatura']["relative_path"])]),
                html.Div([dcc.Link(f"{dash.page_registry['pages.park']['name']}",
                                href=dash.page_registry['pages.park']["relative_path"])]),
                html.Br(),
                html.H5('Autor:'),
                html.Div([
                    html.A("Javier Martínez",
                            href=os.environ["ESGLONBE_LINK"],
                            target="_blank",
                        )],className="esglobe__button"),
                html.Br(),
                html.H5('Tutor:'),
                html.Div([
                    html.A("Isabel Llatas",
                            href=os.environ["ISABEL_LINK"],
                            target="_blank",
                        )],className="isabel__button"),
                            
                ]),
                html.Br(),
                html.Br(),
                html.Div([
                    html.A(href='http://www.usb.ve/',
                           children=[
                            html.Img(src=app.get_asset_url("usb.png"),
                                     className="imag__usb")
                                ]
                    )

                    ])
                

                ],className="left_panel"),
    
    #--
    html.Div([
        dash.page_container
        ],className="right_panel")

],className="wrapper")
#------------------------------


#https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-brain-viewer/app.py
#https://developer.mozilla.org/es/docs/Learn/CSS/CSS_layout/Introduction
#https://plotly.com/python/custom-buttons/


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=port, debug=debug)
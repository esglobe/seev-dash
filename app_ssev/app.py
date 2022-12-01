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
#github_link = os.environ["GITHUB_LINK"]

#------------------------------
app.layout = html.Div([

    #--
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url("ssev-logo.png"))
            ],className="imag__header__title")
        ],className="header__title"),
        
    #--
    html.Div([
        html.H2('SSEV'),
        html.H3('Sistema para el Seguimiento de Ecosistemas Venezolanos')
        ],className="header__info"),

    #--
    html.Div([
        html.H3('Contenido:'),
        html.Div([
                html.Div([dcc.Link(f"{dash.page_registry['pages.home']['name']}",
                                href=dash.page_registry['pages.home']["relative_path"])]),
                html.Div([dcc.Link(f"{dash.page_registry['pages.oni']['name']}",
                                href=dash.page_registry['pages.oni']["relative_path"])]),
                html.Div([dcc.Link(f"{dash.page_registry['pages.park']['name']}",
                                href=dash.page_registry['pages.park']["relative_path"])])
                ]),
        ],className="left_panel"),
    
    #--
    html.Div([
        dash.page_container
        ],className="right_panel")

],className="wrapper")
#------------------------------


#https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-brain-viewer/app.py
#https://developer.mozilla.org/es/docs/Learn/CSS/CSS_layout/Introduction


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=port, debug=debug)
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
        html.H5('header:'),
        ],className="header"),

    #--
    html.Div([
        html.A(href=dash.page_registry['pages.home']["relative_path"],
                children=[
                    html.Img(src=app.get_asset_url("ssev-logo.png"),
                             className="imag__header__title")
            ]),
        html.Br(),
        html.Div([
            html.H1('SSEV'),
            html.H4('Sistema para el Seguimiento de Ecosistemas Venezolanos')
            ]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div([
            html.H3('Contenido:'),
            html.Br(),
            html.Br(),
            html.A(html.H4("1.- Inicio",style={'color':'#FFF'}), href=dash.page_registry['pages.home']["relative_path"]),
            html.Br(),
            html.A(html.H4("2.- Temperatura SST",style={'color':'#FFF'}), href=dash.page_registry['pages.temperatura']["relative_path"]),
            html.Br(),
            html.A(html.H4("3.- Parques",style={'color':'#FFF'}), href=dash.page_registry['pages.park']["relative_path"]),
            html.Br(),
            html.Br()
            ]),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br()
        ],className="sidebar"),

    
    #--
    html.Div([
        html.H5('contenido:'),
        dash.page_container
        ],className="contenido"),

    #--
    html.Div([
        html.Div([
        html.Div([
            html.Br(),
            html.Br(),
            html.A(href='http://www.usb.ve/',
                children=[html.Img(src=app.get_asset_url("usb.png"),
                                className="imag__usb")])
                ]),
            html.H3('Universidad Simón Bolívar')
        ],className="izquierda_vacio"),
        html.Div([
            html.H3('Creadores:'),
            html.Br(),
            html.Br(),
            html.A(html.H5("Autor: Javier Martínez",style={'color':'#000000','text-align': 'left'}), href=os.environ["ESGLONBE_LINK"]),
            html.Br(),
            html.A(html.H5("Tutor: Isabel Llatas",style={'color':'#000000','text-align': 'left'}), href=os.environ["ISABEL_LINK"]),
            html.Br()
            ], className="creadores"),
        html.Div([
                html.H3('Repositorios:'),
                html.Br(),
                html.Br(),
                html.A(html.H5("geet-metview",style={'color':'#000000','text-align': 'left'}), href='https://github.com/esglobe/geet-metview'),
                html.Br(),
                html.A(html.H5("seev-analytics",style={'color':'#000000','text-align': 'left'}), href='https://github.com/esglobe/seev-analytics'),
                html.Br(),
                html.A(html.H5("seev-dash",style={'color':'#000000','text-align': 'left'}), href='https://github.com/esglobe/seev-dash'),
                html.Br()],
        className="repositorios"),
        
        html.Div([
                html.H3('Enlaces de interes:'),
                html.Br(),
                html.Br(),
                html.A(html.H5("Dash",style={'color':'#000000','text-align': 'left'}), href='https://dash.plotly.com/'),
                html.Br(),
                html.A(html.H5("NOAA",style={'color':'#000000','text-align': 'left'}), href='https://www.noaa.gov/'),
                html.Br(),
                html.A(html.H5("Copernicus",style={'color':'#000000','text-align': 'left'}), href='https://www.copernicus.eu/en'),
                html.Br()],
        className="enlaces"),

    ],className="footer")



],className="wrapper")
#------------------------------


#https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-brain-viewer/app.py
#https://developer.mozilla.org/es/docs/Learn/CSS/CSS_layout/Introduction
#https://plotly.com/python/custom-buttons/


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=port, debug=debug)
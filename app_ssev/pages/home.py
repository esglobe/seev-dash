import os
import dash
from dash import html, dcc

dash.register_page(
    __name__,
    name='Home',
    path='/',
    order=0
    #title='Custom Page Title', description='Custom Page Description', image='logo.png'
)


layout = html.Div(children=[
    html.H2(children='Consideraciones iniciales'),

    html.Div(children='''
            El SSEV es un proyecto de investigación destinado al 
            seguimiento y monitoreo del Índice de Vegetación de Diferencia 
            Normalizada (NDVI) de los parques nacionales venezolanos. Surge 
            como iniciativa ante los fenómenos meteorológicos producto del 
            cambio climático y el consecuente cambio global.
            '''),
    html.Br(),
    html.Div(children='''
            El estudio forma parte del Trabajo de Grado presentado a la 
            Universidad Simon Bolivar (USB) como requisito para optar al 
            grado académico de Doctor en Ingeniería. Se espera que los 
            desarrollos teóricos-tecnológicos sean de utilidad en las 
            futuras investigaciones.
        '''),
    html.Br(),
    html.Div([
        html.A("View on GitHub",
                href=os.environ["GITHUB_LINK"],
                target="_blank",
            )],
            className="github__button",
            ),
    html.Br(),
    html.Div([
        html.A("Javier Martínez",
                href=os.environ["ESGLONBE_LINK"],
                target="_blank",
            )],
            className="esglobe__button",
            )

],className="wrapper__home")
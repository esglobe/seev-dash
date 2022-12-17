import os
import dash_gif_component as gif
import dash
from dash import html, dcc

dash.register_page(
    __name__,
    name='Home',
    path='/',
    order=0
    #title='Custom Page Title', description='Custom Page Description', image='logo.png'
)


layout = html.Div([

    html.Div([
        dcc.Markdown("""
        # El Sistema para el Seguimiento de Ecosistemas Venezolanos (SSEV)
         
        El SSEV es un proyecto de investigación destinado al seguimiento y monitoreo del Índice de Vegetación de Diferencia Normalizada (NDVI) de los parques nacionales venezolanos. Un índice de vegetación puede ser definido como un parámetro calculado a partir de los valores de la reflectancia a distintas longitudes de onda, y que es particularmente sensible a la cubierta vegetal. Estos pueden ser usados para determinar la evolución en el tiempo de la cantidad, calidad y desarrollo de la vegetación en las áreas protegidas.
        """),
        html.Br(),
        html.Div([
            html.Img(src='assets/ndvi.jpg',className="imag__ndvi"),
            #html.H6("NDVI para el Norte de Sudamérica producto MOD13Q1 de la NASA.")
        ],className='ndvi__imag',style={'align':'center'}),
        html.Br(),

        dcc.Markdown("""
        La data es recopilada de los servidores de la NASA, Google, NOAA y Copernicus los cuales disponen, de forma gratuita, la información captada por los sensores remotos y dispositivos de teledetección. El objetivo es facilitar la data necesaria para que científicos, investigadores y desarrolladores puedan detectar cambios, mapear tendencias y cuantificar diferencias. 
        
        El proyecto SSEV surge  como iniciativa ante los fenómenos meteorológicos producto del cambio climático y el consecuente cambio global. Numerosos estudios destacan el impacto negativo de la actividad humana en los ecosistemas y señalan que, desde el punto de vista estadístico considerando la tasa actual de consumo de recursos y la estimación más optimista del crecimiento de la tasa tecnológica, la civilización tiene una probabilidad muy baja (menos del 10%) de sobrevivir sin enfrentar un colapso catastrófico. 
        """),
        html.Br(),

        html.Div([
            gif.GifPlayer(gif='assets/rbg.gif',
                    still='assets/rbg.jpg',
                    alt='Reflectancia de superficie terrestre (VNP09GA)'
                    ),
            #html.H6("Reflectancia de la superficie terrestre para el Norte de Sudamérica producto VNP09GA de la NASA.")
        ],className='gif__imag',style={'align':'center'}),
        html.Br(),

        dcc.Markdown("""
        El SSEV forma parte del Trabajo de Grado presentado por Javier Martínez, bajo la tutoría de la Profesora Isabel Llatas, a la Universidad Simon Bolivar (USB) como requisito para optar al grado académico de Doctor en Ingeniería. Se espera que los desarrollos teóricos-tecnológicos sean de utilidad en futuras investigaciones.
        """),
        html.Br(),
        html.Br()
    ])

],className="wrapper__home")
import dash
from dash import dcc, html, Input, Output, ctx, callback

from utils.TEMPERATURA import *


dash.register_page(
    __name__,
    name='Temperatura',
    path='/Temperatura',
    image='ssev-logo.png'
)


# Data temperatura
temperatura = TEMPERATURA()
temperatura.get_data()


#--
layout = html.Div([
        html.H2(children=f"Temperatura promedio en la superficie del mar (SST)"),
        html.H3(children=f"Región El Niño 3.4"),
        html.Div([
            html.Button('SST', id='btn-nclicks-1', n_clicks=0),
            html.Button('Anomalías de SST', id='btn-nclicks-2', n_clicks=0),
            html.Button('ONI', id='btn-nclicks-3', n_clicks=0),
        ],className="btn-gruo-oni"),
        
        html.Div([html.Div(id='container-button-timestamp')]),

        html.Div([
            
            html.Div(children="""Dash: A web application framework for your data.""")
            
        ])
])


@callback(
    Output('container-button-timestamp', 'children'),
    Input('btn-nclicks-1', 'n_clicks'),
    Input('btn-nclicks-2', 'n_clicks'),
    Input('btn-nclicks-3', 'n_clicks')
)
def displayClick(btn1, btn2, btn3):

    height=800
    width=1500

    if "btn-nclicks-1" == ctx.triggered_id:

        graph = temperatura.temperatura_sst(serie='nino34_mean', height=height, width=width)
        return dcc.Graph(id="example-graph", figure=graph)

    elif "btn-nclicks-2" == ctx.triggered_id:

        graph = temperatura.temperatura_sst(serie='anomalias', height=height, width=width)
        return dcc.Graph(id="example-graph", figure=graph)

    elif "btn-nclicks-3" == ctx.triggered_id:
        graph = temperatura.temperatura_oni(height=height, width=width)
        return dcc.Graph(id="example-graph", figure=graph)

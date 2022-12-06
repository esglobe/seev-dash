import dash
from dash import dcc, html, Input, Output, ctx, callback

from utils.PARK_METEOROLOGICAL import *

dash.register_page(
    __name__,
    name='Park',
    path='/Park'
)

# Data temperatura
meteorological = PARK_METEOROLOGICAL()
meteorological.get_parks()
meteorological.get_data()

#--
layout = html.Div([
        html.H2(children=f"Temperatura promedio en la superficie del mar (SST)"),
        html.H3(children=f"Región El Niño 3.4"),
        html.Div([
            html.Button('SST', id='btn-park-1', n_clicks=0),
            html.Button('Anomalías de SST', id='btn-park-2', n_clicks=0),
            html.Button('ONI', id='btn-park-3', n_clicks=0),
        ],className="btn-gruo-park"),
        
        html.Div([html.Div(id='container-button-park')]),

        html.Div([
            
            html.Div(children="""Dash: A web application framework for your data.""")
            
        ])
])


@callback(
    Output('container-button-park', 'children'),
    Input('btn-park-1', 'n_clicks'),
    Input('btn-park-2', 'n_clicks'),
    Input('btn-park-3', 'n_clicks')
)
def displayClick(btn1, btn2, btn3):

    height=700
    width=1200

    if "btn-park-1" == ctx.triggered_id:

        graph = meteorological.localizacion_park(height=height, width=width)
        return dcc.Graph(id="example-graph-1", figure=graph)

    elif "btn-park-2" == ctx.triggered_id:

        graph = meteorological.espacio_temporal_graph(var_group='ndvi_app',
                                                    periodo='2022-02-01',
                                                    height=height,
                                                    width=width)

        return dcc.Graph(id="example-graph-2", figure=graph)

    elif "btn-park-3" == ctx.triggered_id:

        graph = meteorological.time_serie_grafico(serie='ndvi_app',
                                                id_point=2,
                                                height=height,
                                                width=width)
        
        return dcc.Graph(id="example-graph-3", figure=graph)
    
    else:
        graph = meteorological.localizacion_park(height=height, width=width)
        return dcc.Graph(id="example-graph-4", figure=graph)



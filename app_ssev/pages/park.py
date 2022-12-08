import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, ctx, callback

from utils.PARK_METEOROLOGICAL import *

dash.register_page(
    __name__,
    name='Park',
    path='/Park'
)

# Data parque
meteorological = PARK_METEOROLOGICAL()
meteorological.get_parks()
#list_label = [PARK_METEOROLOGICAL.park_format(x) for x in meteorological.parks]
#defaul_park = 'Terepaima'
dropdown_items = [{'value': x,
                   'label': PARK_METEOROLOGICAL.park_format(x) } \
                    for x in meteorological.parks]


#--
layout = html.Div([
        html.H2(children=f"Temperatura promedio en la superficie del mar (SST)"),
        html.H3(children=f"Región El Niño 3.4"),
       
        html.Div([
        dcc.Dropdown(options=dropdown_items, value=meteorological.parks[0], id='dropdown-parks')
                ]),
       
        html.Div([
            html.Button('El Parque', id='btn-park-1', n_clicks=0),
            html.Button('Elevación', id='btn-park-2', n_clicks=0),
            html.Button('Precipitación', id='btn-park-3', n_clicks=0),
            html.Button('NDVI', id='btn-park-4', n_clicks=0)],
        className="btn-gruo-park", id='out-btn-park'),

        html.Div([html.Div(id='out-park')]),

        html.Div([
            
            html.Div(children="""Dash: A web application framework for your data.""")
            
        ])
])


@callback(
    Output('out-btn-park', 'value'),
    Input('dropdown-parks', 'value')
)
def seleccion_parque(value):

    if value not in meteorological.parks:
        return meteorological.parks[0]
    else:
        return value



@callback(
    Output('out-park', 'children'),
    Input('out-btn-park', 'value'),
    Input('btn-park-1', 'n_clicks'),
    Input('btn-park-2', 'n_clicks'),
    Input('btn-park-3', 'n_clicks'),
    Input('btn-park-4', 'n_clicks')
)
def displayClick(valor, btn1, btn2, btn3, btn4):

    height=500
    width=1000

    try:
        park_class = PARK_METEOROLOGICAL()
        park_class.get_data(park=valor)
    except:
        return """ERROR"""
    

    if "btn-park-1" == ctx.triggered_id:

        graph_1 = park_class.localizacion_park(height=height, width=width)
        
        return  [dcc.Graph(id="example-graph-1", figure=graph_1)]

    elif "btn-park-2" == ctx.triggered_id:

        graph_1 = park_class.espacio_temporal_graph(var_group='elevacion_media',
                                                    periodo='2022-02-01',
                                                    height=height,
                                                    width=width)


        return  [dcc.Graph(id="example-graph-2", figure=graph_1)]

    elif "btn-park-3" == ctx.triggered_id:

        graph_1 = park_class.espacio_temporal_graph(var_group='precipitacion_app',
                                                    periodo='2022-02-01',
                                                    height=height,
                                                    width=width)


        graph_2 = park_class.time_serie_grafico(serie='precipitacion_app',
                                                id_point=2, 
                                                height=height,
                                                width=width)                              

        return  [dcc.Graph(id="example-graph-31", figure=graph_1),
                 dcc.Graph(id="example-graph-32", figure=graph_2)]
    
    else:
        graph_1 = park_class.espacio_temporal_graph(var_group='ndvi_app',
                                                    periodo='2022-02-01',
                                                    height=height,
                                                    width=width)

        graph_2 = park_class.time_serie_grafico(serie='ndvi_app',
                                                id_point=2, 
                                                height=height,
                                                width=width) 

        return  [dcc.Graph(id="example-graph-41", figure=graph_1),
                 dcc.Graph(id="example-graph-42", figure=graph_2)]
                   
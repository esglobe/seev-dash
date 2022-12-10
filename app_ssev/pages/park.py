import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, ctx, callback
from datetime import date

from utils.PARK_METEOROLOGICAL import *

dash.register_page(
    __name__,
    name='Park',
    path='/Park'
)

# Data parque
meteorological = PARK_METEOROLOGICAL()
meteorological.get_parks()
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
        className="btn-gruo-park",
        id='out-btn-park'),

        html.Div([
            dcc.DatePickerSingle(id='date-picker',
                                min_date_allowed=date(1970, 1, 1),
                                max_date_allowed=date(2030, 12, 31),
                                initial_visible_month=date(2022, 1, 1),
                                #month_format='D/M/Y',
                                date=date(2022, 1, 1)
                                )
                ]),

        html.Div([html.Div(id='out-park')]),

        html.Div([html.Div(children="""Dash: A web application framework for your data.""")])
])

#--
@callback(
    Output('out-btn-park', 'value'),
    Input('dropdown-parks', 'value')
)
def seleccion_parque(value):

    if value not in meteorological.parks:
        return meteorological.parks[0]
    else:
        return value


#--
@callback(
    Output('out-park', 'children'),
    Input('out-btn-park', 'value'),
    Input('btn-park-1', 'n_clicks'),
    Input('btn-park-2', 'n_clicks'),
    Input('btn-park-3', 'n_clicks'),
    Input('btn-park-4', 'n_clicks'),
    Input('date-picker', 'date')
)
def displayClick(out_btn_parkr, btn_park_1, btn_park_2, btn_park_3, btn_park_4, date_picker):

    height=500
    width=1000

    #--
    try:
        park_class = PARK_METEOROLOGICAL()
        park_class.get_data(park=out_btn_parkr)
        
    except:
        return """ERROR"""

    #--
    try:
        date_object = date.fromisoformat(date_picker)\
                        .strftime('%Y-%m')
        periodo = str(date_object)+'-01'

    except:
        return """ERROR"""
    

    if "btn-park-1" == ctx.triggered_id:

        graph_1 = park_class.localizacion_park(height=height, width=width)
        
        return  [dcc.Graph(id="example-graph-1", figure=graph_1)]

    elif "btn-park-2" == ctx.triggered_id:

        graph_1 = park_class.espacio_temporal_graph(var_group='elevacion_media',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)


        return  [dcc.Graph(id="example-graph-2", figure=graph_1)]

    elif "btn-park-3" == ctx.triggered_id:

        graph_1 = park_class.espacio_temporal_graph(var_group='precipitacion_app',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)


        graph_2 = park_class.time_serie_grafico(serie='precipitacion_app',
                                                height=height,
                                                width=width)                              

        return  [dcc.Graph(id="example-graph-31", figure=graph_1),
                 dcc.Graph(id="example-graph-32", figure=graph_2)]
    
    else:
        graph_1 = park_class.espacio_temporal_graph(var_group='ndvi_app',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)

        graph_2 = park_class.time_serie_grafico(serie='ndvi_app',
                                                height=height,
                                                width=width) 

        return  [dcc.Graph(id="example-graph-41", figure=graph_1),
                 dcc.Graph(id="example-graph-42", figure=graph_2)]
                   
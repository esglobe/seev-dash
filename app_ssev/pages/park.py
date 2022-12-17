import os
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, html, Input, Output, ctx, callback
from datetime import date

from utils.PARK_METEOROLOGICAL import *
from utils.documentacion.spanish import *

responsive = True

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
        dcc.Markdown("""
        # Seguimiento de parques

        EL SSEV es una herramienta diseñada para el seguimiento de la la capa vegetal de los parques nacionales venezolanos a través del Índice de Vegetación de Diferencia Normalizada (NDVI). Con este objeto se entrenan redes neuronales para predecir la variación espacio-temporal del NDVI tomando como variable oxógena a la precipitación total.
        """),
        html.Br(),
        dcc.Markdown("""
        Seleccione el parque de interés:
        """),
        html.Div([
            dcc.Dropdown(options=dropdown_items,
                        value=meteorological.parks[0],
                        id='dropdown-parks')
                ]),
        html.Br(),
        html.Br(),
        html.Div([dcc.Tabs(id="tabs-grafico-parks", value='grafico',            
                            children=[dcc.Tab(label='Características',
                                              value='grafico')]
                    ),
                  html.Div(id='out-park-graf')
                  ], className="out__park__graf"),
        html.Br(),
        html.Br(),
        html.Div([
            dcc.Markdown("""
            ## La precipitación y NDVI

            Seleccione un periodo para la visualización espacial:
            """),
            html.Br(),
            html.Div([
                html.Div([
                daq.NumericInput(
                                min=1,
                                max=12,
                                value=1,
                                label={'label':'Mes'},
                                id='date-month',
                                className='date__month',
                                size=100,
                                labelPosition='bottom'
                                ),
                daq.NumericInput(
                                min=1970,
                                max=2050,
                                value=2022,
                                label={'label':'Año'},
                                id='date-year',
                                className='date__year',
                                size=100,
                                labelPosition='bottom'
                                )
                ],className="date__piker__izquierda"),
                html.Div([


                ],className="date__piker__derecha")

                ],className="date__piker")
                ]),
        html.Br(),
        html.Div([
        dcc.Tabs(id="tabs-parks", value='tab-precipitacion', 
            children=[
                    dcc.Tab(label='Precipitación', value='tab-precipitacion'),
                    dcc.Tab(label='NDVI', value='tab-ndvi'),
                    dcc.Tab(label='Elevación', value='tab-elevacion')
                    ])
        ]),
        html.Br(),
        html.Br(),
        html.Div(id='out-park-tab',className='out__park__tab'),
        html.Br(),
        html.Br()

])


#--
@callback(
    Output('out-park-graf', 'children'),
    Input('dropdown-parks', 'value')
)
def seleccion_parque(value):

    height=600
    width=600

    #--
    try:
        if value not in meteorological.parks:
            park = meteorological.parks[0]
        else:
            park = value

        park_class = PARK_METEOROLOGICAL()
        park_class.get_data_polygon(park=park)

        graph_1 = park_class.localizacion_park(height=height, width=width)

        if value == 'cerro_saroche':
            text_park = text_park_cerro_saroche
        elif value == 'terepaima':
            text_park = text_park_terepaima
        
        return  [html.Br(),
                dcc.Markdown(text_park),
                html.Br(),
                dcc.Graph(id="graph-park", figure=graph_1, responsive=responsive, className="graph__park")]
        
    except:
        return """ERROR"""


#--
@callback(
    Output('out-park-tab', 'children'),
    Input('dropdown-parks', 'value'),
    Input('date-month', 'value'),
    Input('date-year', 'value'),
    Input('tabs-parks', 'value')
)
def displayClick(dropdown_parks, date_month, date_year, tabs_parks):

    height=600
    width=600

    time_height=600
    time_width=900

    #--
    try:
        if dropdown_parks not in meteorological.parks:
            park = meteorological.parks[0]
        else:
            park = dropdown_parks

        park_class = PARK_METEOROLOGICAL()
        park_class.get_data_polygon(park=park)
        park_class.get_data(park=park)
        
    except:
        return """ERROR"""

    #--
    try:
        if date_month<10:
            month = f'0{date_month}'
        else:
            month = f'{date_month}'

        periodo = f'{date_year}-{month}-01'

    except:
        return """ERROR"""

    
    if periodo not in park_class.data_pandas.index.astype(str).to_list():
        return html.H2(f"Información no disponible para el {month}-{date_year}")
    

    #--
    if tabs_parks == 'tab-elevacion':

        graph_1 = park_class.espacio_temporal_graph(var_group='elevacion_media',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)


        return  [
                html.Div([
                html.Br(),
                dcc.Markdown("""### Elevación del parque"""),
                dcc.Graph(id="graph-elevacion", figure=graph_1, responsive=responsive, className="img__espacial")
                ])
                ]

    elif tabs_parks == 'tab-precipitacion':

        graph_1 = park_class.espacio_temporal_graph(var_group='precipitacion_app',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)


        graph_2 = park_class.time_serie_grafico(serie='precipitacion_app',
                                                height=time_height,
                                                width=time_width)                              

        return  [html.Div([
                    html.Br(),
                    dcc.Markdown("""### Visión espacial de la precipitación total (milímetros)"""),
                    dcc.Graph(id="graph-precipitacion-espacial", figure=graph_1,responsive=responsive)
                    ],className="img__espacial"),
                html.Div([
                    dcc.Markdown("""### Serie temporal de la precipitación total (milímetros)"""),
                    dcc.Graph(id="graph-precipitacion-temporal", figure=graph_2,responsive=responsive)
                    ],className="img__temporal")
                ]
    
    elif tabs_parks =='tab-ndvi':

        graph_1 = park_class.espacio_temporal_graph(var_group='ndvi_app',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)

        graph_2 = park_class.time_serie_grafico(serie='ndvi_app',
                                                height=time_height,
                                                width=time_width) 

        return  [html.Div([
                    html.Br(),
                    dcc.Markdown("""### Visión espacial del NDVI"""),
                    dcc.Graph(id="graph-ndvi-espacial", figure=graph_1, responsive=responsive)
                    ],className="img__espacial"),
                html.Div([
                    dcc.Markdown("""### Serie temporal del NDVI"""),
                    dcc.Graph(id="graph-ndvi-temporal", figure=graph_2, responsive=responsive)
                    ],className="img__temporal")
                ]
                   
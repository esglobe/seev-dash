import os
import dash
import dash_bootstrap_components as dbc
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
        # La temperatura promedio en la superficie del mar (SST)

        El Niño-Oscilación del Sur (ENSO), es un fenómeno natural caracterizado por la fluctuación de las temperaturas del océano en la parte central y oriental del Pacífico ecuatorial, asociada a cambios en la atmósfera. El ENSO debe su nombre a sus componentes oceánicas (El Niño y La Niña) y atmosférica (Oscilación del Sur) y es uno de los fenómenos climáticos de mayor influencia a nivel global. El mismo, está relacionado con las anomalías interanuales de las precipitaciones que pueden verse reflejadas en largas sequias o fuertes lluvias. Específicamente, en los países andinos el fenómeno de El Niño causa extensas inundaciones en las zonas costeras de Ecuador, del norte del Perú y el oriente de Bolivia.  Al mismo tiempo, produce sequías en todo el altiplano boliviano-peruano y déficits de lluvias en Colombia y Venezuela. En consecuencia, dada la correlación existente entre el ENSO y la precipitación (que a su vez incide en el crecimiento de la capa vegetal) es relevante dirigir los próximos pasos de la investigación a comprender el origen y posibles causas de este fenómeno.

        En este sentido, el ENSO consta de tres fases: Una Neutra, El Niño (se inicia con un calentamiento a gran escala de las aguas de superficie en la parte central y oriental del Pacífico ecuatorial) y La Niña (se produce un enfriamiento de las temperaturas de la superficie del océano). Las fluctuaciones de las temperaturas oceánicas durante los episodios de El Niño y La Niña van acompañadas de fluctuaciones aún mayores de la presión del aire que se conoce como Oscilación del Sur. Se trata de un movimiento de ida y vuelta, de este a oeste, de masa de aire, entre el Pacífico y la región Indoaustraliana.
        """),
        html.Br(),
        html.Br(),
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
            ## La precipitación y el NDVI en el parque

            Seleccione un periodo en el cual desea evaluar los indicadores espaciales. Los valores de precipitación y NDVI son valores mensuales por lo que solo se considera el año y mes.
            """),
            html.Br(),
            dcc.DatePickerSingle(id='date-picker',
                                min_date_allowed=date(1970, 1, 1),
                                max_date_allowed=date(2030, 12, 31),
                                initial_visible_month=date(2022, 1, 1),
                                #month_format='D/M/Y',
                                date=date(2022, 1, 1)
                                )
                ]),
        html.Br(),
        html.Div([
        dcc.Tabs(id="tabs-parks", value='tab-precipitacion', 
            children=[
                    dcc.Tab(label='Precipitación', value='tab-precipitacion'),
                    dcc.Tab(label='NDVI', value='tab-ndvi'),
                    dcc.Tab(label='Elevación', value='tab-elevacion')
                    ],style={'align':'center'})
        ]),
        html.Br(),
        html.Br(),
        html.Div([html.Div(id='out-park-tab')]),
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
                dcc.Graph(id="graph-park", figure=graph_1, responsive=responsive, className="graph__park")
        ]
        
    except:
        return """ERROR"""



#--
@callback(
    Output('out-park-tab', 'children'),
    Input('dropdown-parks', 'value'),
    Input('date-picker', 'date'),
    Input('tabs-parks', 'value')
)
def displayClick(dropdown_parks, date_picker, tabs_parks):

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
        date_object = date.fromisoformat(date_picker)\
                        .strftime('%Y-%m')
        periodo = str(date_object)+'-01'

    except:
        return """ERROR"""
    
    #--
    if tabs_parks == 'tab-elevacion':

        graph_1 = park_class.espacio_temporal_graph(var_group='elevacion_media',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)


        return  [
            #dcc.Markdown(""""""),
            html.Br(),
            dcc.Markdown("""### Elevación del parque"""),
            dcc.Graph(id="graph-elevacion", figure=graph_1,responsive=responsive)
            ]

    elif tabs_parks == 'tab-precipitacion':

        graph_1 = park_class.espacio_temporal_graph(var_group='precipitacion_app',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)


        graph_2 = park_class.time_serie_grafico(serie='precipitacion_app',
                                                height=time_height,
                                                width=time_width)                              

        return  [
                #dcc.Markdown(""""""),
                html.Br(),
                dcc.Markdown("""### Precipitación espacial"""),
                dcc.Graph(id="graph-precipitacion-espacial", figure=graph_1,responsive=responsive, className="img__precipitacion__espacial"),
                dcc.Markdown("""### Serie temporal de la precipitación en las cuadrículas"""),
                dcc.Graph(id="graph-precipitacion-temporal", figure=graph_2,responsive=responsive)]
    
    elif tabs_parks =='tab-ndvi':

        graph_1 = park_class.espacio_temporal_graph(var_group='ndvi_app',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)

        graph_2 = park_class.time_serie_grafico(serie='ndvi_app',
                                                height=time_height,
                                                width=time_width) 

        return  [#dcc.Markdown(""""""),
                html.Br(),
                dcc.Markdown("""### NDVI espacial"""),
                dcc.Graph(id="graph-ndvi-espacial", figure=graph_1,responsive=responsive, className="img__ndvi__espacial"),
                dcc.Markdown("""### Serie temporal del NDVI en las cuadrículas"""),
                dcc.Graph(id="graph-ndvi-temporal", figure=graph_2,responsive=responsive)]
                   
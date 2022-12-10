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
        html.Div([
            dcc.DatePickerSingle(id='date-picker',
                                min_date_allowed=date(1970, 1, 1),
                                max_date_allowed=date(2030, 12, 31),
                                initial_visible_month=date(2022, 1, 1),
                                #month_format='D/M/Y',
                                date=date(2022, 1, 1)
                                )
                ]),
        html.Br(),
        html.Br(),
        dcc.Tabs(id="tabs-parks", value='tab-park', 
            children=[dcc.Tab(label='El Parque', value='tab-park'),
                    dcc.Tab(label='Elevación', value='tab-elevacion'),
                    dcc.Tab(label='Precipitación', value='tab-precipitacion'),
                    dcc.Tab(label='NDVI', value='tab-ndvi')
                ]),

        html.Div([html.Div(id='out-park')])

])

#--
@callback(
    Output('select-park', 'value'),
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
    Input('select-park', 'value'),
    Input('tabs-parks', 'value'),
    Input('date-picker', 'date')
)
def displayClick(select_park, tabs_parks, date_picker):

    height=600
    width=600

    time_height=600
    time_width=900

    #--
    try:
        park_class = PARK_METEOROLOGICAL()
        park_class.get_data(park=select_park)
        
    except:
        return """ERROR"""

    #--
    try:
        date_object = date.fromisoformat(date_picker)\
                        .strftime('%Y-%m')
        periodo = str(date_object)+'-01'

    except:
        return """ERROR"""
    

    if tabs_parks == 'tab-park':

        graph_1 = park_class.localizacion_park(height=height, width=width)
        
        return  [dcc.Graph(id="example-graph-1", figure=graph_1)]

    elif tabs_parks == 'tab-elevacion':

        graph_1 = park_class.espacio_temporal_graph(var_group='elevacion_media',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)


        return  [dcc.Graph(id="example-graph-2", figure=graph_1)]

    elif tabs_parks == 'tab-precipitacion':

        graph_1 = park_class.espacio_temporal_graph(var_group='precipitacion_app',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)


        graph_2 = park_class.time_serie_grafico(serie='precipitacion_app',
                                                height=time_height,
                                                width=time_width)                              

        return  [dcc.Graph(id="example-graph-31", figure=graph_1),
                 dcc.Graph(id="example-graph-32", figure=graph_2)]
    
    elif tabs_parks =='tab-ndvi':

        graph_1 = park_class.espacio_temporal_graph(var_group='ndvi_app',
                                                    periodo=periodo,
                                                    height=height,
                                                    width=width)

        graph_2 = park_class.time_serie_grafico(serie='ndvi_app',
                                                height=time_height,
                                                width=time_width) 

        return  [dcc.Graph(id="example-graph-41", figure=graph_1),
                 dcc.Graph(id="example-graph-42", figure=graph_2)]
                   
import os
import dash
from dash import dcc, html, Input, Output, ctx, callback

from utils.TEMPERATURA import *

responsive = True

dash.register_page(
    __name__,
    name='Temperatura',
    path='/Temperatura'
)

# Data temperatura
temperatura = TEMPERATURA()
temperatura.get_data()


#--
layout = html.Div([

        dcc.Markdown("""
        # La temperatura promedio en la superficie del mar (SST)

        El Niño-Oscilación del Sur (ENSO), es un fenómeno natural caracterizado por la fluctuación de las temperaturas del océano en la parte central y oriental del Pacífico ecuatorial, asociada a cambios en la atmósfera. El ENSO debe su nombre a sus componentes oceánicas (El Niño y La Niña) y atmosférica (Oscilación del Sur) y es uno de los fenómenos climáticos de mayor influencia a nivel global. El mismo, está relacionado con las anomalías interanuales de las precipitaciones que pueden verse reflejadas en largas sequias o fuertes lluvias. Específicamente, en los países andinos el fenómeno de El Niño causa extensas inundaciones en las zonas costeras de Ecuador, del norte del Perú y el oriente de Bolivia.  Al mismo tiempo, produce sequías en todo el altiplano boliviano-peruano y déficits de lluvias en Colombia y Venezuela. En consecuencia, dada la correlación existente entre el ENSO y la precipitación (que a su vez incide en el crecimiento de la capa vegetal) es relevante dirigir los próximos pasos de la investigación a comprender el origen y posibles causas de este fenómeno.

        En este sentido, el ENSO consta de tres fases: Una Neutra, El Niño (se inicia con un calentamiento a gran escala de las aguas de superficie en la parte central y oriental del Pacífico ecuatorial) y La Niña (se produce un enfriamiento de las temperaturas de la superficie del océano). Las fluctuaciones de las temperaturas oceánicas durante los episodios de El Niño y La Niña van acompañadas de fluctuaciones aún mayores de la presión del aire que se conoce como Oscilación del Sur. Se trata de un movimiento de ida y vuelta, de este a oeste, de masa de aire, entre el Pacífico y la región Indoaustraliana.
        
        """),
        html.Br(),
        html.Br(),
        dcc.Tabs(id="tabs-temp", value='tab-sst', 
            children=[dcc.Tab(label='SST', value='tab-sst'),
                    dcc.Tab(label='Anomalías de SST', value='tab-anomalias'),
                    dcc.Tab(label='ONI', value='tab-oni')
                ]),

        html.Div([html.Div(id='out-tab-temp')],className='out__tab__temp')
])


@callback(
    Output('out-tab-temp', 'children'),
    Input('tabs-temp', 'value')
)
def displayClick(tabs_temp):

    height=600
    width=900

    if tabs_temp == 'tab-sst':

        graph = temperatura.temperatura_sst(serie='nino34_mean', height=height, width=width)
        return [
            dcc.Markdown(""" texto nino34_mean"""),
            dcc.Graph(id="graph_sst", figure=graph,responsive=responsive,className='graph__sst'),
            dcc.Markdown(""" texto """)
            ]

    elif tabs_temp == 'tab-anomalias':

        graph = temperatura.temperatura_sst(serie='anomalias', height=height, width=width)
        return [
            dcc.Markdown(""" texto anomalias"""),
            dcc.Graph(id="graph_anomalias", figure=graph,responsive=responsive,className='graph__anomalias'),
            dcc.Markdown(""" texto """)
        ]

    elif tabs_temp == 'tab-oni':
        graph = temperatura.temperatura_oni(height=height, width=width)
        return [
            dcc.Markdown(""" texto oni"""),
            dcc.Graph(id="graph_oni", figure=graph,responsive=responsive,className='graph__oni'),
            dcc.Markdown(""" texto """)
        ]
    
    else:
        graph = temperatura.temperatura_sst(serie='nino34_mean', height=height, width=width)
        return [
            dcc.Markdown(""" texto nino34_mean"""),
            dcc.Graph(id="example-graph", figure=graph,responsive=responsive),
            dcc.Markdown(""" texto """)
        ]

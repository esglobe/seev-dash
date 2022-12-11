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

    #--
    # html.H1(children='Consideraciones iniciales'),
    # html.Div(children='''
    #         El SSEV es un proyecto de investigación destinado al 
    #         seguimiento y monitoreo del Índice de Vegetación de Diferencia 
    #         Normalizada (NDVI) de los parques nacionales venezolanos. Surge 
    #         como iniciativa ante los fenómenos meteorológicos producto del 
    #         cambio climático y el consecuente cambio global.
    #         '''),
    # html.Br(),
    
    # html.Div([
    #     gif.GifPlayer(gif='assets/rbg.gif',
    #             still='assets/rbg.jpg',
    #             alt='Reflectancia de superficie terrestre (VNP09GA)'),
    # ],className='gif__imag'),
    
    # html.Br(),
    # html.Div(children='''
    #         El estudio forma parte del Trabajo de Grado presentado a la 
    #         Universidad Simon Bolivar (USB) como requisito para optar al 
    #         grado académico de Doctor en Ingeniería. Se espera que los 
    #         desarrollos teóricos-tecnológicos sean de utilidad en las 
    #         futuras investigaciones.
    #         '''),
    html.Div([
        dcc.Markdown("""
        # Consideraciones iniciales


        Uno de los mayores desafíos de la humanidad, es el cambio climático y el consecuente cambio global. Este ha trascendido de la pura investigación científica a un conflicto diario de las distintas sociedades. Numerosos estudios destacan el impacto negativo de la actividad humana en los ecosistemas del Antártico y las incidencias del cambio climático en la acidificación del océano y aguas dulces. Desde el punto de vista estadístico, considerando la tasa actual de consumo de recursos y la estimación más optimista del crecimiento de la tasa tecnológica, se concluye que la civilización tiene una probabilidad muy baja (menos del 10%) de sobrevivir sin enfrentar un colapso catastrófico. Evidentemente, estos efectos traen consigo consecuencias devastadoras en la biodiversidad.

        Ante esta problemática, el Consejo de Derechos Humanos de las Naciones Unidas ha declarado, como derecho universal, el acceso a un medio ambiente limpio y saludable en su resolución A/HRC/RES/48/13. Por lo que, los distintos países, han puesto en marcha el diseño de propuestas, normativas y acciones que por ahora no han sido suficientes para contrarrestar la crisis. América Latina y el Caribe, no escapan de esta realidad esta región se caracteriza por poseer regulaciones y marcos legales débiles y en muchos casos son pobremente ejecutados. Igualmente, la falta concreta de indicadores en la medición de las políticas públicas y planes estratégicos, impide el cálculo del progreso, la evaluación de resultados y por tanto, la incorporación de los ajustes necesarios.

        Específicamente, Venezuela, es un país petrolero que forma parte de los 17 países Megadiversos por su abundante variedad en especies como animales, plantas y ecosistemas. De acuerdo a su ubicación geográfica, se contempla al mismo tiempo una región amazónica, andina, atlántica, caribeña y llanera. Entre su diversidad de ambientes se puede mencionar, los arrecifes coralinos, sabanas, tepuyes, mochimales, entre otros.  En general, el 16% del territorio nacional venezolano está constituido por 79 áreas protegidas (43 parques nacionales y 36 monumentos naturales). La administración y cuidado de estas zonas históricamente ha sido concedida al Poder Público Nacional.

        Desde hace varias décadas, universidades y entes gubernamentales venezolanos han realizado investigaciones con el objeto de explicar las causas y consecuencias de fenómenos climatológicos a través de las mediciones de temperatura, precipitación y humedad detectadas con los módulos meteorológicos instalados en el territorio nacional. Sin embargo, el reciente desarrollo tecnológico y el crecimiento de las redes de comunicación ha permitido implementar algoritmos avanzados y disponer de información que en el pasado parecía imposible. Entre estos, se puede mencionar a las imágenes capturadas por los satélites destinados al seguimiento de la atmósfera y a la superficie terrestre.
        """),
        html.Br(),

        html.Div([
            gif.GifPlayer(gif='assets/rbg.gif',
                    still='assets/rbg.jpg',
                    alt='Reflectancia de superficie terrestre (VNP09GA)'
                    ),
        ],className='gif__imag',style={'align':'center'}),
        html.Br(),

        dcc.Markdown("""
        Organizaciones como la NASA (National Aeronautics and Space Administration) y compañías como Google, disponen de forma gratuita información captada por los sensores remotos y dispositivos de teledetección mediante plataformas dinámicas que permiten a científicos, investigadores y desarrolladores detectar cambios, mapear tendencias y cuantificar diferencias en la superficie de la Tierra. En consecuencia, se ha generado un especial interés por la combinación de las bandas espectrales y, específicamente, en los índices de vegetación. Un índice de vegetación puede ser definido como un parámetro calculado a partir de los valores de la reflectancia a distintas longitudes de onda, y que es particularmente sensible a la cubierta vegetal. Estos índices pueden ser para determinar la evolución en el tiempo de la cantidad, calidad y desarrollo de la vegetación en las áreas protegidas.

        A la fecha de esta investigación, Venezuela no cuenta con un plan nacional de mitigación y adaptación al cambio climático ni con un sistema de seguimiento que utilice los avances tecnológicos en el área de teledetección y sensores remotos para la salud de la capa vegetal, resguardo y conocimiento de los ecosistemas más vulnerables. En tal sentido, la presente investigación está orientada al diseño de una plataforma web que permita a las autoridades identificar factores estacionales y planificar estrategias que busquen resguardar la biodiversidad venezolana ante amenazas climatologías y/o presencia de actividades humanas. Entre los principales desafíos se puede mencionar el desarrollo de una metodología escalable a la variedad de ecosistemas y ambientes venezolanos, así como la transferencia del alto volumen de datos y la velocidad de los procesos de estimación.

        Entre los principales desafíos que presenta esta investigación se puede mencionar el desarrollo de una metodología escalable a la variedad de ecosistemas y ambientes venezolanos, así como el volumen de datos que deben ser transferidos y la velocidad de los procesos de estimación. Para solventar estas limitantes, se han utilizado bases de datos no relacionales como MongoDB que permitieron alcanzar niveles adecuados de velocidad en la transferencia de datos. Del mismo modo, se implementó Docker en la construcción de una plataforma basada en la arquitectura de microservicios, donde sea posible dividir las tareas en pequeños servicios independientes. Vale la pena destacar que, a excepción de MongoDB, los softwares utilizados en este estudio son gratuitos y tienen documentación de libre acceso para su aplicación en la enseñanza, investigación científica, desarrollo de productos y creación de plataformas web.
        """),
        html.Br(),

        dcc.Markdown("""
            ## Justificación e importancia

            La presente investigación está sustentada en el Artículo 127 de la Constitución de la República Bolivariana de Venezuela y el Artículo 4 de la Ley Orgánica del Ambiente. En estos se resalta la corresponsabilidad entre el Estado y los ciudadanos en la protección del medio ambiente venezolano.

            Del mismo modo, la Ley Orgánica del Ambiente en su Artículo 10 plantea que la Autoridad Nacional Ambiental es responsable de estimular la creación de mecanismos que promuevan y fomenten la investigación científica y estimulen la educación ambiental. Mientras, los artículos 23 y 85 establecen que se utilizará a la investigación como base fundamental para el lineamiento de los planes ambientales y que el estudio del impacto ambiental constituye el sustento de las decisiones ambientales. En el Artículo 75 y 76 se plantea que el Estado promoverá, apoyará y consolidará proyectos de investigación dirigidos al conocimiento de los ecosistemas y la diversidad biológica, con la finalidad de comprender sus potencialidades, beneficios y limitaciones.

            Así mismo, la presente se justifica en la Declaración de Cancún de Países Megadiversos Afines, donde los países participantes (entre ellos Venezuela) declaran su preocupación por las limitaciones de los distintos instrumentos internacionales para proteger eficazmente la biodiversidad, y reconocen a las zonas tropicales y subtropicales como las más vulnerables ante cambios climáticos e intervenciones humanas.

            Los lineamientos legales antes señalados declaran la responsabilidad conjunta del Estado y ciudadanía en el cuidado y resguardo del medio ambiente. Además, consideran a la investigación científica como basamento para el desarrollo de planes estratégicos y en la toma de decisiones de gran impacto ambiental. 
            """),


        html.Div([
            html.Img(src='assets/ndvi.jpg',className="imag__ndvi"),
        ],className='ndvi__imag',style={'align':'center'}),

        dcc.Markdown("""
        ## Objetivos

        A partir de lo anteriormente expuesto, la presente investigación tiene por objetivo general desarrollar una plataforma de visualización y modelaje estadístico para el seguimiento evolutivo del índice de vegetación y variables climatológicas en los principales parques nacionales venezolanos, usando información recopilada por sensores remotos y dispositivos de teledetección.

        Para lograr este objetivo general, se proponen los siguientes objetivos específicos:

        1. Desarrollar una metodología escalable mediante la definición de cuadrantes o grillas que tomen en consideración las características de los parques nacionales venezolanos. 
        2. Diseñar una base de datos para el almacenamiento de la información de sensores remotos y dispositivos de teledetección según los cuadrantes y áreas delimitadas. 
        3. Proponer y ajustar modelos estadísticos para el pronóstico del índice de vegetación, a partir de variables climatológicas, en particular, modelos basados en utilización de redes neuronales, tales como el modelo autoregresivo no lineal de entrada exógena (NARX).
        4. Desarrollar una plataforma web con una arquitectura de microservicios que permita la visualización del pronóstico del índice de vegetación y los valores de las variables climatológicas más relevantes para el estudio de las regiones delimitadas.
        """),
        html.Br(),
        html.Br()
    ])

],className="wrapper__home")
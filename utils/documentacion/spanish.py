
##
# TEMPERATURA
##

text_temperatura_sst = """
## La temperatura promedio en la superficie del mar (SST) región El Nino 3.4

Dada la incidencia de El ENSO en los eventos climáticos globales surge la necesidad de  encontrar mecanismos que permitan, primeramente, llevar un seguimiento de su evolución en el tiempo para luego realizar estimaciones o pronósticos. En el proyecto SSEV se monitorea la temperatura promedio en la superficie del mar (SST) específicamente en la región El Niño 3.4 por ser el área idónea en el estudio de El ENSO. La base de datos es recopilada de los servidores de NOAA y las predicciones son alcanzadas con el entrenamiento de redes neuronales recurrentes de celda LSTM.
"""

text_temperatura_anomalias = """
## Las anomalías SST

Las anomalías SST son el resultado de la comparación entre la temperatura observada en la región El Niño 3.4 y la temperatura normal en la zona para el periodo base correspondiente (promedios mensuales de 30 años). El proceso desarrollado en SSEV utiliza los pronósticos SST alcanzados tras el entrenamiento de redes neuronales recurrentes y las temperaturas de los periodos base pautados por NOAA para predecir las anomalías SST.
"""

text_temperatura_oni = """
## El Índice Niño Oceánico (ONI)

El ONI es el principal índice utilizado por NOAA en el seguimiento de EL ENSO. El mismo es definido como el promedio móvil de tres meses de las anomalías de temperatura en la superficie del mar del Pacifico tropical centro-oriental (región Niñó 3.4). NOAA considera que las condiciones de El Niño están presentes en el océano cuando el ONI, en la región Niño 3.4, es igual a 0.5 o más, lo cual implica que las aguas superficiales del Pacifico tropical centro-oriental son 0.5 grados Celsius más cálidas en comparación con el promedio en la zona. De manera análoga, las condiciones de La Niña existen cuando el ONI es igual a -0.5 o menor, indicando que la región es 0.5 grados más fría que el promedio.
"""
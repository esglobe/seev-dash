import json
import geopandas
from pyproj.crs import CRS
import pandas as pd
from datetime import datetime

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import math

import os

from utils.MONGO import CONEXION

class PARK_METEOROLOGICAL:
    """
    Clase para la graficos de precipitacio, ndvi del parque
    """

    COLECCION = 'SSEV'
    PAST_YEARS = 15

    PRECI_CRS = CRS.from_wkt('GEOGCS["Coordinate System imported from GRIB file",DATUM["unnamed",SPHEROID["Sphere",6367470,0]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST]]')

    #--
    def park_format(x = 'cerrosaroche'):
        """
        Funcion para el nopmbre de los parques
        """

        try:

            park_name = ' '.join([x.capitalize() for x in  x.split('_')])
        except:
            park_name = None

        return park_name

    #--
    def get_parks(self):
        """
        Fucnion para identificar a los parques
        """

        # Creando la conexión con MongoDB
        mongoConexion = CONEXION.conexion()
        db = mongoConexion[PARK_METEOROLOGICAL.COLECCION]

        # Parks
        parks = db.estimateMeteorological.distinct("park")
        self.parks = [x for x in parks]
        self.parks_formato = [PARK_METEOROLOGICAL.park_format(x) for x in self.parks]

        # Cerrando conexion
        mongoConexion.close()

    #--
    def get_data(self,park='terepaima'):
        """
        Funcion para descargar base de datos
        """

        # Creando la conexión con MongoDB
        mongoConexion = CONEXION.conexion()
        db = mongoConexion[PARK_METEOROLOGICAL.COLECCION]
        time_filter = (datetime.today()-pd.DateOffset(months=PARK_METEOROLOGICAL.PAST_YEARS*12))\
                            .toordinal()

        #----
        # Data meteorologica
        #----
        park_data = db.estimateMeteorological.find({'park':park,'time':{'$gte':time_filter}},
                                                    {'id_point':1,
                                                    'latitud':1,
                                                    'longitud':1,
                                                    'time':1,
                                                    'elevacion_media':1,
                                                    'ndvi_media':1,
                                                    'ndvi_prediction':1,
                                                    'precipitacion_mm':1,
                                                    'precipitacion_narx':1,
                                                    'prediction_ann':1,
                                                    'type':1,
                                                    'time_actualizacion':1
                                                    })

        # Generando pandas dataframe
        data_pandas = pd.DataFrame([file for file in park_data])
        data_pandas['periodo'] = data_pandas.time.apply(lambda x: datetime.fromordinal(x))
        data_pandas.index = pd.to_datetime(data_pandas.periodo)
        data_pandas['precipitacion_app'] = data_pandas.apply(lambda x: x.precipitacion_narx if x.type=='prediction' else x.precipitacion_mm,1)
        data_pandas['ndvi_app'] = data_pandas.apply(lambda x: x.ndvi_prediction if x.type=='prediction' else x.ndvi_media,1)

        self.data_pandas = data_pandas.sort_index()


        # centroides
        self.centroides = self.data_pandas\
                .reset_index(drop=True)\
                .groupby(['id_point','latitud','longitud'], as_index=False)\
                .count()\
                .sort_values('id_point')


        # ndvi
        self.id_poin_ndvi = self.data_pandas[['id_point','ndvi_app']]\
                            .dropna()\
                            .reset_index(drop=True)\
                            .sort_values('id_point')\
                            .id_point.unique().tolist()

        #precipitacion
        self.id_poin_preci = self.data_pandas[['id_point','precipitacion_app']]\
                            .dropna()\
                            .reset_index(drop=True)\
                            .sort_values('id_point')\
                            .id_point.unique().tolist()

        #---
        # Data poligonos
        #---
        # db_polygons = db.polygons.find({'park':park})
        # self.polygons = [polygon for polygon in db_polygons]

        # # Poligono del parque
        # geoJson_polygon = json.dumps( self.polygons[0]['polygons']['polygon'] )
        # geopandas_polygon = geopandas.read_file(geoJson_polygon)
        # self.park_poligono = geopandas_polygon.to_crs(PARK_METEOROLOGICAL.PRECI_CRS)

        # Cerrando conexion
        mongoConexion.close()
    
    
    #--
    def get_data_polygon(self,park='terepaima'):
        """
        Datos de poligono dle parque
        """     
        mongoConexion = CONEXION.conexion()
        db = mongoConexion[PARK_METEOROLOGICAL.COLECCION]   

        db_polygons = db.polygons.find({'park':park})
        self.polygons = [polygon for polygon in db_polygons]

        # Poligono del parque
        geoJson_polygon = json.dumps( self.polygons[0]['polygons']['polygon'] )
        geopandas_polygon = geopandas.read_file(geoJson_polygon)
        self.park_poligono = geopandas_polygon.to_crs(PARK_METEOROLOGICAL.PRECI_CRS)

        # Cerrando conexion
        mongoConexion.close()


    #--
    def get_data_raster(self, var_group = 'elevacion_media', periodo = '2022-01-01'):
        """
        Funcion para crear la data delk raster
        """
        
        import xarray
        
        # Variable precipitacion, elevacion o NDVI
        if var_group == 'elevacion_media':
            var_id = ['id_point','latitud','longitud']
            data_tempo = self.data_pandas\
                            .reset_index(drop=True)\
                            .groupby(var_id, as_index=False)\
                            .agg({var_group:'max'})\
                            .sort_values('id_point')

            dataDate = 20211216

        else:
            var_id = ['id_point','latitud','longitud','periodo','time']
            data_tempo = self.data_pandas\
                            .reset_index(drop=True)\
                            .groupby(var_id, as_index=False)\
                            .agg({var_group:'max', 'time':'max'})\
                            .sort_values(['id_point','periodo'])\
                            .query(f"periodo=='{periodo}'")

            dataDate = int(data_tempo.time.unique()[0])

        centroide_y = data_tempo.latitud.unique()
        centroide_x = data_tempo.longitud.unique()
        media = data_tempo[var_group].tolist()

        # Documentos
        fieldset = [{
                    "gridType": "regular_ll",
                    "Nx": len(centroide_x),
                    "Ny": len(centroide_y),
                    "distinctLatitudes": centroide_y,
                    "distinctLongitudes": centroide_x,
                    "paramId": 1,
                    "shortName": var_group,
                    "values": media,
                    "dataDate": dataDate,
                    "dataTime": 1200
                    }
                    ]

        ds_rect = xarray.open_dataset(fieldset, engine="cfgrib")
        ds_rect = ds_rect.rio.write_crs(PARK_METEOROLOGICAL.PRECI_CRS)\
        
        return ds_rect

    #--
    def espacio_temporal_graph(self,var_group,periodo,height=750, width=750):
      """
      Funcion para la graficacion de terepaima
      """

      ds_rect = self.get_data_raster(var_group = var_group, periodo = periodo)
      exterior_coords = self.park_poligono\
                          .exterior[0]\
                          .coords.xy

      value_min = self.data_pandas\
                      .query(f"periodo=='{periodo}'")[var_group]\
                      .min()
      value_min = math.floor(100*value_min)/100

      value_max = self.data_pandas\
                      .query(f"periodo=='{periodo}'")[var_group]\
                      .max()
      value_max = math.ceil(100*value_max)/100


      if var_group == 'elevacion_media':
          #levels=[200, 400, 600, 800, 1000, 1200, 1400,1600, 1800, 2000]
          n_range_colorbar = 10

          list_values = np.arange(value_min, value_max, (value_max-value_min)/n_range_colorbar)
          levels = list(map(int,list(list_values)))

          range_color = [min(levels),max(levels)]
          cmap='Purples'
          x_name = ''#'Elevación (m)'
          yaxis_title = 'Latitud'
          xaxis_title = 'Longitud'
          tickformat= None

      if var_group == 'precipitacion_app':

          n_range_colorbar = 10
          #levels=[0,0.2,0.4,0.6,0.8,1,1.2]
          list_values = np.arange(value_min, value_max, (value_max-value_min)/n_range_colorbar)
          levels = list_values#list(map(int,list(list_values)))

          range_color = [min(levels),max(levels)]
          cmap='Blues'
          x_name = ''#'Precipitación total (mm)'
          yaxis_title = 'Latitud'
          xaxis_title = 'Longitud'
          tickformat= ".1f"

      if var_group == 'ndvi_app':
          levels=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
          range_color = [min(levels),max(levels)]
          cmap='Greens'
          x_name = ''#'NDVI'
          yaxis_title = 'Latitud'
          xaxis_title = 'Longitud'
          tickformat= ".1f"


      # centroides
      delta = 0.02
      centroides = self.centroides.values.tolist()


      fig = px.imshow(ds_rect[var_group], 
                      origin='lower',
                      color_continuous_scale=cmap,
                      range_color=range_color)


      fig.update_yaxes(showline=True,
                      linewidth=0,
                      linecolor='black',
                      gridcolor='#FFFFFF',
                      mirror=True,
                      ticks="outside",
                      tickwidth=2,
                      tickcolor='#5C2B05',
                      tickformat= ".1f",
                      ticklen=10)

      fig.update_xaxes(showline=True,
                      linewidth=0,
                      linecolor='black',
                      gridcolor='#FFFFFF',
                      mirror=True,
                      ticks="outside",
                      tickwidth=2,
                      tickcolor='#5C2B05',
                      tickformat= ".1f",
                      ticklen=10)

      for i in list(range(0, len(centroides) )):
          fig.add_trace(go.Scatter(x=[centroides[i][2]],y=[centroides[i][1]],
                                  text=str(int(centroides[i][0])),
                                  mode="text",
                                  name=f'Punto id {str(int(centroides[i][0]))}',
                                  showlegend=False,
                                  textfont_color='red'
                                  ))

      fig.add_trace(go.Scatter(x=list(exterior_coords[0]),
                              y=list(exterior_coords[1]),
                                  line=dict(
                                          color="#001B32",
                                          width=2,
                                      ),
                              showlegend=False))


      fig.update_layout(
          coloraxis_colorbar=dict(title=x_name,
                                  tickvals=levels,
                                  orientation="v",
                                  tickformat= tickformat),
          yaxis_title=yaxis_title,
          xaxis_title=xaxis_title,
          font = dict(size = 14),
          height=height,
          width=width,
          uniformtext_minsize=8,
          uniformtext_mode='hide',
          plot_bgcolor='rgba(0,0,0,0)'
      )

      return fig

    #--
    def localizacion_park(self, height=500, width=750):
      """
      Funcion para el grafico de la localicacion del parque
      """

      centroide = self.park_poligono.geometry[0].centroid.coords.xy

      print(os.environ['MAPBOX_TOKEN'])

      fig = go.Figure(go.Scattermapbox(
          mode = "markers",
          lon = [centroide[1][0]], lat = [centroide[0][0]],
          marker = {'size': 20, 'color': ["cyan"]}))

      fig.update_layout(
        #   mapbox_style="white-bg",
          mapbox = {
            'accesstoken' : os.environ['MAPBOX_TOKEN'],
            #   'style': "stamen-terrain",
              'center': { 'lon': centroide[0][0], 'lat': centroide[1][0]},
              'zoom': 9, 'layers': [{
                  'source': self.polygons[0]['polygons']['polygon'],
                  'type': "fill", 
                  'below': "traces", 
                  'color': "#655F5F"}]
              },
          margin = {'l':0, 'r':0, 'b':0, 't':0},
          height=height,
          width=width

      )

      return fig


    #--
    def time_serie_grafico(self, serie, height=800, width=1500):

        """
        Funcion para la grafica precipitacion y ndvi temporal
        """

        data_temperatura = self.data_pandas\
                            .sort_index()\
                            .copy()

        pd_training = data_temperatura\
                        .query("type!='prediction'")\
                        .sort_index()[[serie,'id_point']]\
                        .dropna()
        pd_forecast = data_temperatura\
                        .query("type=='prediction'")\
                        .sort_index()[[serie,'id_point']]\
                        .dropna()

        if serie == 'precipitacion_app':
            name_serie = 'Precipitación total (mm)'
            name_forecast = 'Pronóstico Precipitación'
            xaxis_title='Mes'
            yaxis_title='Precipitación total (mm)'
            line_training=dict(color='#0036FF', width=2)
            line_prediction=dict(color='#0099E5', width=2,dash='dash')
            marker_symbol='star'
            marker_line_color='#0099E5'
            marker_color='#0099E5'
            id_poins = self.id_poin_preci

        if serie == 'ndvi_app':
            name_serie = 'NDVI'
            name_forecast = 'Pronóstico NDVI'
            xaxis_title='Mes'
            yaxis_title='NDVI'
            line_training=dict(color='#008345', width=2)
            line_prediction=dict(color='#1EBD72', width=2,dash='dash')
            marker_symbol='star'
            marker_line_color='#1EBD72'
            marker_color='#1EBD72'
            id_poins = self.id_poin_ndvi
            
        else:
            name_serie = ''
            name_forecast = ''

        fig = go.Figure(layout=go.Layout(plot_bgcolor='rgba(0,0,0,0)'))

        list_update = []
        for id in id_poins:

            fig.add_trace(go.Scatter(x=pd_training.query(f'id_point=={id}').index,
                                    y=pd_training.query(f'id_point=={id}')[serie],
                                    mode='lines',
                                    name=name_serie,
                                    line=line_training,
                                    xperiodalignment="middle"
                                    ))
            fig.add_trace(go.Scatter(x=pd_forecast.query(f'id_point=={id}').index,
                                    y=pd_forecast.query(f'id_point=={id}')[serie],
                                    mode='lines+markers',
                                    name=name_forecast,
                                    marker_symbol=marker_symbol,
                                    marker_line_width=3,
                                    marker_size=3,
                                    marker_line_color=marker_line_color,
                                    marker_color=marker_color,
                                    line=line_prediction,
                                    xperiodalignment="middle"
                                    ))

            list_arg = (2*len(id_poins)-2)*[False]
            list_arg.insert((id-1),True)
            list_arg.insert(id,True)

            list_update.append(dict(label=f' {id}  ',
                                    method="update",
                                    args=[{'visible':list_arg}]
                                    )
                                )


        list_update.insert(0,
                        dict(label=f' All ',
                            method="update",
                            args=[{'visible':(2*len(id_poins))*[True]}]
                            )
                        )

        # linea de pronostico
        fig.add_vline(x=pd_training.index.max(),
                    line_width=3,
                    line_dash="dash",
                    line_color="#580606")


        fig.update_xaxes(tickformat="%Y/%m",
                        showline=True,
                        linewidth=1,
                        linecolor='black',
                        gridcolor='#E4E4E4',
                        mirror=True,
                        ticks="outside",
                        tickwidth=2,
                        tickcolor='#5C2B05',
                        ticklen=10
                        )

        fig.update_yaxes(showline=True,
                        linewidth=1,
                        linecolor='black',
                        gridcolor='#E4E4E4',
                        mirror=True,
                        ticks="outside",
                        tickwidth=2,
                        tickcolor='#5C2B05',
                        ticklen=10)

        fig.update_traces(textfont_size=14)

        fig.update_layout(showlegend=False,
                        xaxis_title=xaxis_title,
                        yaxis_title=yaxis_title,
                        legend_title_text='Serie',
                        legend_title = dict( font = dict(size = 30)),
                        legend=dict(y=0.5,
                                    traceorder='reversed',
                                    font_size=11),
                        uniformtext_minsize=8,
                        uniformtext_mode='hide',
                        height=height,
                        width=width,
                        font = dict(size = 14),
                        xaxis=dict(
                            range = [pd_forecast.index.max()- pd.DateOffset(months=5*12), pd_forecast.index.max() + pd.DateOffset(months=1)],
                            rangeselector=dict(
                                x=0,
                                y=1.1,
                                buttons=list([
                                    dict(count=1,
                                        label="1-años",
                                        step="year",
                                        stepmode="backward"),
                                    dict(count=2,
                                        label="2-años",
                                        step="year",
                                        stepmode="backward"),
                                    dict(count=5,
                                        label="5-años",
                                        step="year",
                                        stepmode="todate"),
                                    dict(count=10,
                                        label="10-años",
                                        step="year",
                                        stepmode="backward")
                                    #dict(step="all",label="Todo")
                                ])),

                            rangeslider=dict(visible=True),
                            type="date"),
                        updatemenus=[dict(type="dropdown",
                                        direction="down",
                                        bgcolor='Dark Blue',
                                        buttons=list(list_update),
                                        #active=id_poins[0],
                                        showactive=True,
                                        xanchor="right",
                                        x=1.1,
                                        yanchor="top",
                                        y=1.3
                                        )]
                            
                            )

        fig.update_layout(
            annotations=[
                        dict(text="Punto:",
                            x=1,
                            xref="paper",
                            y=1.3,
                            yref="paper",
                            showarrow=False,
                            align="left",)
                        ])

        return fig    
from datetime import datetime
import pandas as pd

import plotly.graph_objects as go
from plotly.graph_objects import Layout

from utils.MONGO import CONEXION

class TEMPERATURA:
    """
    Clase para graficos del panel de temperatura
    """

    COLECCION = 'SSEV'

    #--
    def get_data(self):
        """
        Funcion para descargar base de datos
        """

        # Creando la conexión con MongoDB
        mongoConexion = CONEXION.conexion()
        db = mongoConexion[TEMPERATURA.COLECCION]

        # Realizando consulta
        sst_data = db.estimateSSTNino34.find({},{'data_pandas':1,
                                                'anomalias':1,
                                                'time_actualizacion':1,
                                                'time':1,
                                                'nino34_mean':1,
                                                'oni':1,
                                                'type':1})

        # Generando pandas dataframe
        data_pandas = pd.DataFrame([file for file in sst_data])
        data_pandas['periodo'] = data_pandas.time.apply(lambda x: datetime.fromordinal(x))
        data_pandas.index = pd.to_datetime(data_pandas.periodo)
        self.data_pandas = data_pandas.sort_index()

        # Cerrando conexion
        mongoConexion.close()
    
    #--
    def temperatura_sst(self, serie, height=800, width=1500):
        """
        Funcion para la grafica de temperatura y anomalias SST
        """

        data_temperatura = self.data_pandas.copy()

        pd_training = data_temperatura\
                        .query("type=='' | type=='training'")\
                        .sort_index()[[serie]].dropna().round(2)
        pd_forecast = data_temperatura\
                        .query("type=='prediction'")\
                        .sort_index()[[serie]].dropna().round(2)



        if serie == 'nino34_mean':
            name_serie = 'SST'
            name_forecast = 'Pronóstico SST'
            xaxis_title='Mes'
            yaxis_title='Temperatura SST (°C)'
            line_training=dict(color='#E74A01', width=2)
            line_prediction=dict(color='#F68A00', width=2,dash='dash')
            marker_symbol='star'
            marker_line_color='#F68A00'
            marker_color='#F68A00'

        if serie == 'anomalias':
            name_serie = 'Anomalía SST'
            name_forecast = 'Pronóstico Anomalía SST'
            xaxis_title='Mes'
            yaxis_title='Anomalía SST (°C)'
            line_training=dict(color='#F91243', width=2)
            line_prediction=dict(color='#FA3ABA', width=2,dash='dash')
            marker_symbol='star'
            marker_line_color='#FA3ABA'
            marker_color='#FA3ABA'
            
        else:
            name_serie = ''
            name_forecast = ''


        fig = go.Figure(layout=Layout(plot_bgcolor='rgba(0,0,0,0)'))
        fig.add_trace(go.Scatter(x=pd_training.index,
                                y=pd_training[serie],
                                mode='lines',
                                name=name_serie,
                                line=line_training,
                                xperiodalignment="middle"
                                ))
        fig.add_trace(go.Scatter(x=pd_forecast.index,
                                y=pd_forecast[serie],
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

        fig.update_traces(textfont_size=18)

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
                        font = dict(size = 22),
                        xaxis=dict(
                            range = [pd_forecast.index.max()- pd.DateOffset(months=5*12), pd_forecast.index.max() + pd.DateOffset(months=1)],
                            rangeselector=dict(
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
                            type="date")
                            
                            )

        return fig

    #--
    def temperatura_oni(self, serie = 'oni', height=800, width=1500):
        """
        Funcion para el grafico del pronostico del ONI
        """
        
        pd_oni = self.data_pandas[[serie,'type']].copy()\
                    .sort_index()\
                    .dropna()\
                    .copy()

        pd_oni[serie] = pd_oni[serie].round(2)

        data_fig = pd_oni[ pd_oni.index < pd_oni.index.max() ].copy()
        data_fig['color'] = data_fig['oni'].apply(lambda x: 0 if x<0 else 1)

        max_date = data_fig.index.max() + pd.DateOffset(months=5) 

        fig = go.Figure(layout=Layout(plot_bgcolor='rgba(0,0,0,0)'))
        fig.add_trace(go.Scatter(x=data_fig.index.tolist(), y=len(data_fig.index.tolist())*[0],
                                mode='lines',name='NIÑO3.4 NARX entrenamiento',
                                line=dict(color='#B0ACAC', width=2),
                                fill = 'tozeroy',
                                fillcolor = '#F5FF8D',
                                showlegend=False))

        fig.add_trace(go.Scatter(x=data_fig.index, 
                                y=data_fig.oni,
                                mode='lines+markers',
                                marker_symbol='x-thin',
                                marker_line_width=2,
                                marker_size=3,
                                marker_line_color='#003CAF',
                                marker_color='#003CAF',
                                name='NIÑO3.4 NARX entrenamiento',
                                line=dict(color='#0057FF', width=3),
                                fill = 'tonexty',
                                fillcolor = '#8FB5FE',
                                showlegend=False
                                ))

        # pronostico
        fig.add_trace(go.Scatter(x=data_fig[data_fig.type=='prediction'].index, 
                                y=data_fig[data_fig.type=='prediction'].oni,
                                textposition="bottom right",
                                marker_symbol='star',
                                marker_line_width=3,
                                marker_size=3,
                                marker_line_color='#0057FF',
                                marker_color='#0057FF',
                                mode='lines+markers+text',
                                name='NIÑO3.4 NARX entrenamiento',
                                line=dict(color='#EF02F3', width=3),
                                showlegend=False
                                ))

        fig.add_hline(y=0.5, line_width=0.75, line_dash="dash", line_color="#FF6C6C")
        fig.add_hline(y=1, line_width=1, line_dash="dash", line_color="#FF3F3F")
        fig.add_hline(y=1.5, line_width=1.25, line_dash="dash", line_color="#FF0000")
        fig.add_hline(y=2, line_width=1.50, line_dash="dash", line_color="#D70000")


        fig.add_hline(y=2.5, line_width=1.75, line_dash="dash", line_color="#AD0000")

        fig.add_hline(y=-0.5, line_width=0.75, line_dash="dash", line_color="#69A6FF")
        fig.add_hline(y=-1, line_width=1, line_dash="dash", line_color="#6979FF")
        fig.add_hline(y=-1.5, line_width=1.25, line_dash="dash", line_color="#3F53FF")
        fig.add_hline(y=-2, line_width=1.5, line_dash="dash", line_color="#001BFF")
        fig.add_hline(y=-2.5, line_width=1.75, line_dash="dash", line_color="#00059A")

        # linea de pronostico
        fig.add_vline(x=data_fig[data_fig.type=='prediction'].index.min(), 
        line_width=3,
        line_dash="dash",
        line_color="#580606")


        fig.update_xaxes(tickformat="%Y/%m",showline=True, linewidth=1, linecolor='black', gridcolor='#E4E4E4',mirror=True,
                        ticks="outside", tickwidth=2, tickcolor='#5C2B05', ticklen=10)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='#E4E4E4',mirror=True,
                        ticks="outside", tickwidth=2, tickcolor='#5C2B05', ticklen=10)

        fig.update_traces(textfont_size=14)
        fig.update_layout(#title="""
        #                         Índice Niño Oceánico (ONI) pronóstico periodo {date_init} al {date_fin}
        #                         <br><sup>Promedio de 3-meses para las anomalías SST en la región Niño 3.4 (variación periodos base de 30-años)
        #                         </sup>
        #                         """.format(date_init=str(data_fig[data_fig.type=='prediction'].index.min().strftime('%Y/%m')),
        #                                 date_fin=str(data_fig[data_fig.type=='prediction'].index.max().strftime('%Y/%m')) ),
                        xaxis_title='Mes',
                        yaxis_title='Promedio 3-Meses anomalías SST (°C)',
                        uniformtext_minsize=8,
                        uniformtext_mode='hide',
                        height=height,
                        width=width,
                        font = dict(size = 22),
                        xaxis=dict(
                                    range = [data_fig[data_fig.type=='prediction'].index.max()- pd.DateOffset(months=5*12), data_fig[data_fig.type=='prediction'].index.max() + pd.DateOffset(months=1)],
                                    rangeselector=dict(
                                        buttons=list([
                                            dict(count=1,
                                                label="1-años",
                                                step="year",
                                                stepmode="backward"),
                                            dict(count=2,
                                                label="2-años",
                                                step="year",
                                                stepmode="backward"),
                                            dict(count=7,
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
                                    type="date")
                        )

        return fig
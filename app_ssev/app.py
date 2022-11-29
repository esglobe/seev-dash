import os
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from flask import Flask

from utils.MONGO import CONEXION
from datetime import datetime

debug = True
port = os.environ["PORT"]

# Server/app
server = Flask(__name__)
app = Dash(__name__, server=server)

# Creando la conexión con MongoDB
db = CONEXION.conexion()
db.list_collection_names()

# Fecha actual
time = datetime.today().toordinal()

# Realizando consulta
sst_data = db.SSTNino34.find({"time":{"$lte":time}})

# Generando pandas dataframe
data_pandas = pd.DataFrame([file for file in sst_data])
data_pandas['periodo'] = data_pandas.time.apply(lambda x: datetime.fromordinal(x))
data_pandas['mes_year'] =  data_pandas['periodo'].dt.strftime('%B-%Y')
data_pandas.index = pd.to_datetime(data_pandas.periodo)


# grafico
graph = px.line(data_pandas, x="periodo", y="nino34_mean")

app.layout = html.Div(
    children=[
        html.H1(
            children=f"Hello Dash in 2022 from {'Dev Server' if debug else 'Prod Server'}"
        ),
        html.Div(children="""Dash: A web application framework for your data."""),
        dcc.Graph(id="example-graph", figure=graph),
    ]
)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=port, debug=debug)
import os
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from flask import Flask

# from utils.MONGO import CONEXION
# from utils.UTILS import *
# from datetime import datetime

debug = True
port = os.environ["PORT"]

server = Flask(__name__)
app = Dash(__name__, server=server)


data = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)

graph = px.bar(data, x="Fruit", y="Amount", color="City", barmode="group")

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
import dash
from dash import html, dcc

dash.register_page(
    __name__,
    name='Precipitacion',
    path='/Precipitacion'
    #title='Custom Page Title', description='Custom Page Description', image='logo.png'
)


layout = html.Div(children=[
    html.H1(children='This is our Home page'),

    html.Div(children='''
        This is our Home page content.
    '''),

])
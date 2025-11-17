from dash import html, dcc, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/lap-analysis")

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H5("Hi there")
        ),
        dbc.Col(
            html.H5("Hi there")
        ),
        dbc.Col(
            html.H5("Hi there")
        ),
    ]),

    dbc.Row([
        dbc.Col(
            html.H5("Hi there")
        ),
        dbc.Col(
            html.H5("Hi there")
        ),
        dbc.Col(
            html.H5("Hi there")
        ),
    ]),
])
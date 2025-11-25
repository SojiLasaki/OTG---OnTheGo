import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import os
import pandas as pd

# datasets = [maps for maps in os.listdir("../../Datasets") if not maps.startswith(".")]
# datasets_capitalized = [folder.capitalize() for folder in datasets]

search = dbc.Container([
    # html.Br(className="mb-1"),
    dbc.Row([
        html.H6("Indianapolis 2025",  style={ "textAlign": "center"}),
        html.Hr(),
        dbc.Col([
            html.P("Race"),
            dcc.Dropdown(
                id="race-dropdown",
                options=[
                    {"label": "Race 1", "value": "Race 1"},
                    {"label": "Race 2", "value": "Race 2"},
                ],
                placeholder="Select Race",
                clearable=False,
                persistence=True,
                persistence_type='session',
            )],
            width=6,
            className="mb-3",
        ),
        dbc.Col([
            html.P("Vehicle Number"),
            dcc.Dropdown(
                id="vehicle-dropdown",
                placeholder="Select Vehicle",
                clearable=False,
                # style={"backgroundColor": "#000000", "color": "#ffffff"},
                persistence=True,
                persistence_type='session',
            )],
            width=6,
            className=""
        ),
    ], className="justify-content-center"),

    dbc.Row(
        dbc.Col(
            html.Div(
                html.Button("Search", 
                            className="btn w-100"), 
                className="d-flex justify-content-center align-items-center text-align-center",
                style={"border":"1px solid grey", "hover":"background-color"},
                id="search-btn"
            ),
            width=12,
            className="mx-auto"
        )
    ),
], className="g-0")
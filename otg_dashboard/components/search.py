import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import os
import pandas as pd

datasets = [maps for maps in os.listdir("../Datasets") if not maps.startswith(".")]
datasets_capitalized = [folder.capitalize() for folder in datasets]

search = dbc.Container([
    # html.Br(className="mb-1"),
    dbc.Row([
        dbc.Col([
            html.P("Map"),
            dcc.Dropdown(
                id="map-dropdown",
                options = datasets_capitalized,
                placeholder="Select Map",
                clearable=False,
                persistence_type='session',
            )],
            width=4,
            className="mb-3",
        ),
        dbc.Col([
            html.P("Race"),
            dcc.Dropdown(
                id="race-dropdown",
                placeholder="Select Race",
                clearable=False,
                persistence_type='session',
            )],
            width=4,
            className="mb-3",
        ),
        dbc.Col([
            html.P("Vehicle Number"),
            dcc.Dropdown(
                id="vehicle-dropdown",
                options=[
                    {"label": "Driver A", "value": "driver_a"},
                    {"label": "Driver B", "value": "driver_b"},
                    {"label": "Driver C", "value": "driver_c"},
                ],
                placeholder="Select Vehicle",
                clearable=False,
                # style={"backgroundColor": "#000000", "color": "#ffffff"},
                persistence_type='session',
            )],
            width=4,
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
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# import numpy as np
# from dash import register_page, html, dcc
# import os
# import dash_bootstrap_components as dbc


# register_page(__name__, path="/")

# layout = dbc.Container([
#     dcc.Store(id="session-store"),  #stores datat  between pages
#     dbc.Row([
#         dbc.Col([
#             html.Div([
#             html.H4("Race Overview"),
#             html.Hr(),
#         ], className="align-items-center justofy-content-center mx-auto")
#         ]), 
#         dbc.Col([
#             html.H6("Table")
#         ])
#     ]),
#     table = dash_table.DataTable(
#         data=race_results.to_dict("records"),
#         columns=[{"name": i, "id": i} for i in race_results.columns],
#         page_size=10,
#         style_table={"overflowX": "auto"},
#         style_cell={"textAlign": "center", "backgroundColor": "#111", "color": "white"},
#         style_header={"backgroundColor": "#333", "fontWeight": "bold"},
#     ),
#     dbc.Card(
#         dbc.CardBody([
#             html.H5(f"Race Results — {selected_map} / {selected_race}", className="text-center"),
#             table
#         ]),
#         className="mt-3 shadow-sm bg-dark text-white"
#     )
# ], className="g-0")


# # load data
# time = np.linspace(0,60,600)
# root = "../"
# df = pd.read_csv(f'{root}Datasets/Road America/Race 1/26_Weather_Race 1_Anonymized.csv', sep=';')


import dash_bootstrap_components as dbc
from dash import register_page, html, dcc

register_page(__name__, path="/")

layout = dbc.Container([
    dcc.Store(id="session-store"),  # shared session data

    dbc.Row([
        dbc.Col([
            html.H5("Race Overview", className="text-center text-white "),
            html.Hr()
        ])
    ]),

    dbc.Row([
        dbc.Col(html.Div(id="overview-summary"), width=12)
    ]),

    dbc.Row([
        dbc.Col(html.Div(id="overview-table"), width=12, className="")
    ]),
], fluid=True, className="p-4 text-white")

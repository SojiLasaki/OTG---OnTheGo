from dash import html, register_page, dcc
import dash_bootstrap_components as dbc

register_page(__name__, path="/")

layout = html.Div([

])

layout = dbc.Container([
    dbc.Row(
        dbc.Col([
            html.Div([
                html.Div([
                    html.P("We process data On The Go",  className="text-center text-white mb-3 justify-content-center"),
                    html.H3("On The Go", className="text-center mb-1 text-white justify-content-center"),
                ], className="mb-5"),
                html.H5("Make a selection", className="text-center text-white mb-3 justify-content-center"),
                ],className="d-flex flex-column justify-content-center align-items-center ",
                style={"marginTop" :"100px"}
            ),
        ])
    ),

    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id="race-dropdown",
                options=[
                    {"label": "Race 1", "value": "race_1"},
                    {"label": "Race 2", "value": "race_2"},
                    {"label": "Race 3", "value": "race_3"},
                ],
                placeholder="Select a Race",
                clearable=False,
                persistence_type='session',
            ),
            width=4,
            className="mb-3",
        ),
        dbc.Col(
            dcc.Dropdown(
                id="driver-dropdown",
                options=[
                    {"label": "Driver A", "value": "driver_a"},
                    {"label": "Driver B", "value": "driver_b"},
                    {"label": "Driver C", "value": "driver_c"},
                ],
                placeholder="Select a Driver",
                clearable=False,
                # style={"backgroundColor": "#000000", "color": "#ffffff"},
                persistence_type='session',
            ),
            width=4,
            className="mb-3"
        ),
    ], className="justify-content-center"),

    dbc.Row(

    ),


    dbc.Row(
        dbc.Col(
            html.Div([
                html.Hr(className="mt-6"),
                html.Br(className="mt-6")
            ]),
        )
    ),
])
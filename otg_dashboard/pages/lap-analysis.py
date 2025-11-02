import dash_bootstrap_components as dbc
from dash import register_page, html, dcc

register_page(__name__, path="/lap-analysis")


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

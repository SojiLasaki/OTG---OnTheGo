from dash import html, dcc, register_page, Output, Input, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from components.search import search

register_page(__name__, path="/")

layout = dbc.Container([
    search,
    dcc.Store(id="session-store"),

    # WRAPPER THAT CAN BE HIDDEN
    html.Div([
        html.H6('Weather Review', className="mt-4, mb-2"),
        dbc.Row([
            dbc.Col(dcc.Graph(id="air-temp-chart"), width=3),
            dbc.Col(dcc.Graph(id="track-temp-chart"), width=3),
            dbc.Col(dcc.Graph(id="humidity-chart"), width=3),
            dbc.Col(dcc.Graph(id="pressure-chart"), width=3),
        ], className="g-1")
    ], id="weather-wrapper"),

    dbc.Row([
        dbc.Col([html.H5("Race Overview", className="mt-3 text-center text-white"), html.Hr()])
    ]),

    dbc.Row([dbc.Col(html.Div(id="overview-summary"), width=12)]),
    dbc.Row([dbc.Col(html.Div(id="overview-table"), width=12)])
], fluid=True, id="weather-wrapper", style={"margin": "0", "padding": "0"})


def make_figure(df, col, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=df[col],
        mode="lines+markers",
        text=[f"WIND_DIRECTION: {wd}" for wd in df["WIND_DIRECTION"]],
        hovertemplate='%{y}<br>%{text}<extra></extra>'
    ))
    fig.update_layout(
        template="plotly_dark",
        title=title,
        height=250,
        margin=dict(l=10, r=10, t=60, b=10)
    )
    return fig


@callback(
    Output("air-temp-chart", "figure"),
    Output("track-temp-chart", "figure"),
    Output("humidity-chart", "figure"),
    Output("pressure-chart", "figure"),
    Output("weather-wrapper", "style"),   # <-- NEW OUTPUT
    Input("session-store", "data")
)
def update_weather_charts(data):
    if not data:
        # Hide graph container
        hidden = {"display": "none"}
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), hidden

    race = data["race"]
    csv_path = f"../../Datasets/indianapolis/{race}/26_weather_{race}.csv"
    df = pd.read_csv(csv_path, sep=";")

    visible = {}  # show wrapper

    return (
        make_figure(df, "AIR_TEMP", "Air Temp"),
        make_figure(df, "TRACK_TEMP", "Track Temp"),
        make_figure(df, "HUMIDITY", "Humidity"),
        make_figure(df, "PRESSURE", "Pressure"),
        visible
    )

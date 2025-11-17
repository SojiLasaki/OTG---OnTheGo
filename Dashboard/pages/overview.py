from dash import html, dcc, register_page
import dash_bootstrap_components as dbc
import pandas as pd
from components.search import search
import plotly.graph_objs as go
# Register the page
register_page(__name__, path="/")

selected_race = "Race 1"
# --- Load CSV ---
df = pd.read_csv(f"../../Datasets/Indianapolis/Race 1/26_weather_{selected_race}.csv", sep=";")

# --- Create figures ---
weather_air_temp = go.Figure()
weather_track_temp = go.Figure()
weather_humidity = go.Figure()
weather_pressure = go.Figure()

# --- Traces ---
weather_air_temp.add_trace(go.Scatter(
    y=df["AIR_TEMP"],
    mode="lines+markers",
    name="AIR_TEMP",
    text=[f"WIND_DIRECTION: {wd}" for wd in df["WIND_DIRECTION"]],
    hovertemplate='%{y} %{name}<br>%{text}<br>Time: %{x}<extra></extra>'
))

weather_track_temp.add_trace(go.Scatter(
    y=df["TRACK_TEMP"],
    mode="lines+markers",
    name="TRACK_TEMP",
    text=[f"WIND_DIRECTION: {wd}" for wd in df["WIND_DIRECTION"]],
    hovertemplate='%{y} %{name}<br>%{text}<br>Time: %{x}<extra></extra>'
))

weather_humidity.add_trace(go.Scatter(
    y=df["HUMIDITY"],
    mode="lines+markers",
    name="HUMIDITY",
    text=[f"WIND_DIRECTION: {wd}" for wd in df["WIND_DIRECTION"]],
    hovertemplate='%{y} %{name}<br>%{text}<br>Time: %{x}<extra></extra>'
))

weather_pressure.add_trace(go.Scatter(
    y=df["PRESSURE"],
    mode="lines+markers",
    name="PRESSURE",
    text=[f"WIND_DIRECTION: {wd}" for wd in df["WIND_DIRECTION"]],
    hovertemplate='%{y} %{name}<br>%{text}<br>Time: %{x}<extra></extra>'
))

# --- Layout (shared settings) ---
for fig in [weather_air_temp, weather_track_temp, weather_humidity, weather_pressure]:
    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=60, b=10),
        height=250
    )

weather_air_temp.update_layout(title="Air Temp")
weather_track_temp.update_layout(title="Track Temp")
weather_humidity.update_layout(title="Humidity")
weather_pressure.update_layout(title="Pressure")

# --- Dash Layout ---
layout = dbc.Container([
    search,
    html.H6('Weather Review', className="mb-2"),

    dbc.Row([
        dbc.Col(dcc.Graph(figure=weather_air_temp, style={"height": "250px"}), width=3),
        dbc.Col(dcc.Graph(figure=weather_track_temp, style={"height": "250px"}), width=3),
        dbc.Col(dcc.Graph(figure=weather_humidity, style={"height": "250px"}), width=3),
        dbc.Col(dcc.Graph(figure=weather_pressure, style={"height": "250px"}), width=3),
    ], className="g-1"),

    dcc.Store(id="session-store"),  # shared session data

    dbc.Row([
        dbc.Col([
            html.H5("Race Overview", className="mt-3 text-center text-white "),
            html.Hr()
        ])
    ]),

    dbc.Row([
        dbc.Col(html.Div(id="overview-summary"), width=12)
    ]),

    dbc.Row([
        dbc.Col(html.Div(id="overview-table"), width=12, className="")
    ]),
], 
fluid=True, 
style={"margin": "0", "padding": "0"})

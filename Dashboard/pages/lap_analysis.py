from dash import html, dcc, register_page, Output, Input, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from components.search import search

register_page(__name__, path="/lap-analysis")

layout = dbc.Container([
    search,
    dcc.Store(id="session-store"),
    dbc.Row([ 
        dbc.Col(
            html.Div([
                html.H6("Driver Infomation:"),
                html.Hr(),
                html.Div([
                    html.Div([
                        html.H6("Driver Number: 33"),
                        html.H6("|", className="px-3"),
                        html.H6("Name: Micheal Edwards"),
                        html.H6("|", className="px-3"),
                        html.H6("Position: 11"),
                        html.H6("|", className="px-3"),
                        html.H6("Status: Classified"),
                        html.H6("|", className="px-3"),
                        # html.H6("Vehicle Number: 021"),
                        # html.H6("|", className="px-3"),
                        html.H6("Vehicle: Toyota GR86"),
                        html.H6("|", className="px-3"),
                        html.H6("Team: Eagles Canyon Racing Powered by Fast Track"),
                        html.H6("|", className="px-3"),
                        html.H6("Laps: 23"),
                        html.H6("|", className="px-3"),
                        html.H6("Country: USA"),
                ], className="ms-auto d-flex")
                ], className="d-flex w-100"),
                html.Hr(),
                html.P("", id="driver_name")
            ]),
        ),
    ], className="mt-4"),
    dbc.Row([
        dbc.Col([
            html.H6("Select Lap"),
            dcc.Slider(
                    min = 1,
                    max = 23,
                    step = 1,
                    id = "lap_slider",
                    marks = None,
                    tooltip={"placement": "bottom", "always_visible": True, "style": {"color": "white", "fontSize": "10px" }},
                ),
                html.Div([
                    dbc.Col(dcc.Graph("Lap Analysis Chart"), id="lap_analysis"), 
                    html.Hr() 
            ], id="lap_analysis_wrapper", style={"margin":"0", "padding":"0"}),
        ]), 
    ])
])


def make_figure(df, col, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=df[col],
        mode="lines",
        text=[f"telemetry_value: {wd}" for wd in df["telemetry_value"]],
        hovertemplate='%{y}<br>%{text}<extra></extra>'
    ))
    fig.update_layout(
        template="plotly_dark",
        title=title,
        height=250,
        margin=dict(l=10, r=10, t=60, b=10)
    )
    return fig


# @callback(
#     Output("lap_analysis", "figure"),
#     Output("lap_analysis_wrapper", "style"),
#     Input("session-store", 'data')
# )
# def update_lap_analysis(data):
#     if not data:
#         hidden = {'display': "none"}
#         return go.Figure(), hidden
    
#     if data["race"] == "Race 1":
#         race_abriv = "R1"
#     else:
#         race_abriv = "R2"
        
#     race = data["race"]
#     csv_path = f"../../Datasets/indianapolis/{race}/{race_abriv}_indianapolis_motor_speedway_telemetry.CSV"
#     df = pd.read_csv(csv_path, sep=";")
#     print(df.head(1))
#     visible = {}

#     return (
#         make_figure(df, "telemetry_value", "telemetry_value"),
#         visible
#     )

# @callback(
#     Input("session-data"),
#     Output("driver_info")

# )


@callback(
    Output("lap_analysis", "figure"),
    Output("lap_analysis_wrapper", "style"),
    Input("session-store", "data"),
    Input("lap_slider", "value")
)
def update_lap_analysis(data, selected_lap):
    # Hide when no session data yet
    if not data:
        return go.Figure(), {"display": "none"}

    # Determine Race abbreviation
    race_abriv = "R1" if data["race"] == "Race 1" else "R2"

    # Load telemetry CSV
    csv_path = (
        f"../../Datasets/indianapolis/{data['race']}/"
        f"{race_abriv}_indianapolis_motor_speedway_telemetry.CSV"
    )
    df = pd.read_csv(csv_path, sep=";")

    # ---- FILTER BY SELECTED LAP ----
    df_lap = df[df["lap"] == selected_lap]

    # If selected lap has no data → hide
    if df_lap.empty:
        return go.Figure(), {"display": "none"}

    # ---- FILTER TELEMETRY TYPE (default: speed) ----
    # You can change Speed → Throttle, Brake, RPM etc.
    df_speed = df_lap[df_lap["telemetry_name"] == "Speed"]

    if df_speed.empty:
        return go.Figure(), {"display": "none"}

    # Create figure
    fig = make_figure(df_speed, "telemetry_value", f"Speed — Lap {selected_lap}")

    return fig, {"display": "block"}

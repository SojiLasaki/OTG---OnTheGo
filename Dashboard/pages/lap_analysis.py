from dash import html, dcc, register_page, Output, Input, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from components.search import search
import os

register_page(__name__, path="/lap-analysis")

# ------------------------------------------------------------
# TELEMETRY CHANNELS
# ------------------------------------------------------------
ENGINE_CHANNELS = ["speed", "nmot"]
PEDAL_CHANNELS = ["aps", "pbrake_f", "pbrake_r"]
GFORCE_CHANNELS = ["accx_can", "accy_can"]

HOVER_EXTRA = [
    "Steering_Angle",
    "Laptrigger_lapdist_dls",
    "VBOX_Long_Minutes",
    "VBOX_Lat_Min",
]

# ------------------------------------------------------------
# PAGE LAYOUT
# ------------------------------------------------------------
layout = dbc.Container([
    search,
    dcc.Store(id="session-store"),
    # ---------------- DRIVER INFO ----------------
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("Driver Information:"),
                html.Hr(),
                html.Div([
                    html.Div([
                        html.H6(["Number: ", html.Span(id="driver_number")]),
                        html.H6("|", className="px-3"),
                        html.H6(["Name: ", html.Span(id="driver_name")]),
                        html.H6("|", className="px-3"),
                        html.H6(["Position: ", html.Span(id="driver_position")]),
                        html.H6("|", className="px-3"),
                        html.H6(["Status: ", html.Span(id="driver_status")]),
                        html.H6("|", className="px-3"),
                        html.H6(["Vehicle: ", html.Span(id="driver_vehicle")]),
                        html.H6("|", className="px-3"),
                        html.H6(["Team: ", html.Span(id="driver_team")]),
                        html.H6("|", className="px-3"),
                        html.H6(["Laps: ", html.Span(id="driver_laps")]),
                        html.H6("|", className="px-3"),
                        html.H6(["Country: ", html.Span(id="driver_country")]),
                    ], className="ms-auto d-flex", style={"margin":"auto"})
                ], className="d-flex w-100"),
                html.Hr()
            ])
        )
    ], className="mt-4"),
    html.H6("Select Lap"),

    dcc.Slider(
        min=1, max=23, step=1, id="lap_slider",
        marks=None,
        tooltip={"placement": "bottom", "always_visible": True},
    ),

    html.Hr(),

    # ----------- ROW 1: Speed + RPM -----------------
    dbc.Row([
        dbc.Col(dcc.Graph(id="speed_graph", style={"height": "300px"}), md=6),
        dbc.Col(dcc.Graph(id="rpm_graph", style={"height": "300px"}), md=6),
    ]),

    # ----------- ROW 2: Throttle + Brake F + Brake R --------
    dbc.Row([
        dbc.Col(dcc.Graph(id="throttle_graph", style={"height": "300px"}), md=4),
        dbc.Col(dcc.Graph(id="brake_f_graph", style={"height": "300px"}), md=4),
        dbc.Col(dcc.Graph(id="brake_r_graph", style={"height": "300px"}), md=4),
    ]),

    # ----------- ROW 3: ACCX + ACCY -----------------
    dbc.Row([
        dbc.Col(dcc.Graph(id="accx_graph", style={"height": "300px"}), md=6),
        dbc.Col(dcc.Graph(id="accy_graph", style={"height": "300px"}), md=6),
    ]),

], fluid=True)


@callback(
    Output("speed_graph", "figure"),
    Output("rpm_graph", "figure"),
    Output("throttle_graph", "figure"),
    Output("brake_f_graph", "figure"),
    Output("brake_r_graph", "figure"),
    Output("accx_graph", "figure"),
    Output("accy_graph", "figure"),
    Input("session-store", "data"),
    Input("lap_slider", "value"),
)
def update_lap_graphs(data, lap):

    empty = go.Figure().update_layout(template="plotly_dark")

    if not data or lap is None:
        return empty, empty, empty, empty, empty, empty, empty

    race = data.get("race")
    driver = data.get("vehicle")
    if not race or not driver:
        return empty, empty, empty, empty, empty, empty, empty

    csv_path = f"../../telemetry_split/{race}/driver_{driver}/lap_{lap}.csv"
    print("Loading:", csv_path)

    if not os.path.exists(csv_path):
        print("CSV missing")
        return empty, empty, empty, empty, empty, empty, empty

    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["telemetry_value"] = pd.to_numeric(df["telemetry_value"], errors="coerce")

    # ---------------------- FIXED HOVER VALUES ----------------------
    # Convert each HOVER_EXTRA telemetry into a dictionary keyed by timestamp
    hover_data = {}

    for hov in HOVER_EXTRA:
        hov_df = df[df["telemetry_name"] == hov]
        hover_data[hov] = dict(zip(hov_df["timestamp"], hov_df["telemetry_value"]))

    # ---------------------- COLOR SET ----------------------
    COLORS = {
        "speed": "#1f77b4",
        "nmot": "#ff7f0e",
        "aps": "#2ca02c",
        "pbrake_f": "#d62728",
        "pbrake_r": "#9467bd",
        "accx_can": "#8c564b",
        "accy_can": "#e377c2",
    }

    # ----------- Helper: build a single channel chart -----------
    def build_chart(channel, title):
        sub = df[df["telemetry_name"] == channel]

        if sub.empty:
            return empty

        # Build customdata row-by-row properly
        customdata = []
        for ts in sub["timestamp"]:
            customdata.append([
                hover_data["Steering_Angle"].get(ts),
                hover_data["Laptrigger_lapdist_dls"].get(ts),
                hover_data["VBOX_Long_Minutes"].get(ts),
                hover_data["VBOX_Lat_Min"].get(ts),
            ])

        fig = go.Figure()

        fig.add_trace(go.Scattergl(
            x=sub["timestamp"],
            y=sub["telemetry_value"],
            mode="lines",
            name=channel,
            line=dict(color=COLORS.get(channel, "#FFFFFF")),
            customdata=customdata,
            hovertemplate=(
                "Time: %{x}<br>"
                f"{channel}: %{{y}}<br><br>"
                "Steering: %{customdata[0]}<br>"
                "Lap Dist: %{customdata[1]}<br>"
                "VBOX Long: %{customdata[2]}<br>"
                "VBOX Lat: %{customdata[3]}<br>"
            ),
        ))

        fig.update_layout(
            template="plotly_dark",
            title=title,
            margin=dict(l=10, r=10, t=40, b=10),
        )

        return fig

    # ----------- Build all 7 charts -----------
    speed_fig = build_chart("speed", "Speed (km/h)")
    rpm_fig = build_chart("nmot", "RPM")
    throttle_fig = build_chart("aps", "Throttle (%)")
    brake_f_fig = build_chart("pbrake_f", "Brake Front (%)")
    brake_r_fig = build_chart("pbrake_r", "Brake Rear (%)")
    accx_fig = build_chart("accx_can", "ACC X (G)")
    accy_fig = build_chart("accy_can", "ACC Y (G)")

    return speed_fig, rpm_fig, throttle_fig, brake_f_fig, brake_r_fig, accx_fig, accy_fig


# ============================================================
# DRIVER INFO CALLBACK (unchanged)
# ============================================================
@callback(
    Output("driver_number", "children"),
    Output("driver_name", "children"),
    Output("driver_position", "children"),
    Output("driver_status", "children"),
    Output("driver_vehicle", "children"),
    Output("driver_team", "children"),
    Output("driver_laps", "children"),
    Output("driver_country", "children"),
    Input("session-store", "data")
)
def update_driver_info(data):
    if not data:
        return [""] * 8

    csv_path = f"../../Datasets/indianapolis/{data['race']}/03_results.CSV"
    df = pd.read_csv(csv_path, sep=";")

    row = df[df["NUMBER"] == int(data["vehicle"])].iloc[0]

    return (
        row["NUMBER"],
        f"{row['DRIVER_FIRSTNAME']} {row['DRIVER_SECONDNAME']}",
        row["POSITION"],
        row.get("STATUS", ""),
        row["VEHICLE"],
        row["TEAM"],
        row["LAPS"],
        row["DRIVER_COUNTRY"],
    )

# load graph on search
@callback(
    Output("lap_slider", "value"),
    Input("session-store", "data")
)
def initialize_lap_slider(data):
    if not data:
        return None  # No race loaded yet
    return 1  # Default lap to 1 whenever data is loaded

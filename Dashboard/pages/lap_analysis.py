# from dash import html, dcc, register_page, Output, Input, callback
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.graph_objs as go
# from components.search import search

# register_page(__name__, path="/lap-analysis")

# # ============================================================
# # PAGE LAYOUT
# # ============================================================
# layout = dbc.Container([
#     search,
#     dcc.Store(id="session-store"),

#     # ---------------- DRIVER INFO ----------------
#     dbc.Row([
#         dbc.Col(
#             html.Div([
#                 html.H6("Driver Information:"),
#                 html.Hr(),
#                 html.Div([
#                     html.Div([
#                         html.H6(["Number: ", html.Span(id="driver_number")]),
#                         html.H6("|", className="px-3"),
#                         html.H6(["Name: ", html.Span(id="driver_name")]),
#                         html.H6("|", className="px-3"),
#                         html.H6(["Position: ", html.Span(id="driver_position")]),
#                         html.H6("|", className="px-3"),
#                         html.H6(["Status: ", html.Span(id="driver_status")]),
#                         html.H6("|", className="px-3"),
#                         html.H6(["Vehicle: ", html.Span(id="driver_vehicle")]),
#                         html.H6("|", className="px-3"),
#                         html.H6(["Team: ", html.Span(id="driver_team")]),
#                         html.H6("|", className="px-3"),
#                         html.H6(["Laps: ", html.Span(id="driver_laps")]),
#                         html.H6("|", className="px-3"),
#                         html.H6(["Country: ", html.Span(id="driver_country")]),
#                     ], className="ms-auto d-flex")
#                 ], className="d-flex w-100"),
#                 html.Hr()
#             ])
#         )
#     ], className="mt-4"),

#     # ---------------- LAP + GRAPH ----------------
#     dbc.Row([
#         dbc.Col([
#             html.H6("Select Lap"),
#             dcc.Slider(
#                 min=1, max=23, step=1, id="lap_slider",
#                 marks=None,
#                 tooltip={"placement": "bottom", "always_visible": True,
#                          "style": {"color": "white", "fontSize": "10px"}}
#             ),
#             html.Div([
#                 dbc.Col(dcc.Graph(id="lap_analysis")),
#                 html.Hr()
#             ], id="lap_analysis_wrapper", style={"margin": "0", "padding": "0"}),
#         ])
#     ])
# ])

# # ============================================================
# # FIGURE MAKER
# # ============================================================
# def make_figure(df, col, title):
#     fig = go.Figure()

#     fig.add_trace(go.Scattergl(
#         x=df["timestamp"],
#         y=df[col],
#         mode="lines",
#         line=dict(width=2, color=df["timestamp"], colorscale="Viridis"),
#         text=[
#             f"Speed: {v}<br>"
#             f"Lap: {l}<br>"
#             f"Time: {t}"
#             for v, l, t in zip(df[col], df["lap"], df["timestamp"])
#         ],
#         hovertemplate="%{text}<extra></extra>"
#     ))

#     fig.update_layout(
#         template="plotly_dark",
#         title=title,
#         height=300,
#         margin=dict(l=10, r=10, t=50, b=10)
#     )
#     return fig


# # ============================================================
# # UPDATE LAP FIGURE
# # ============================================================
# @callback(
#     Output("lap_analysis", "figure"),
#     Output("lap_analysis_wrapper", "style"),
#     Input("session-store", "data"),
#     Input("lap_slider", "value")
# )
# def update_lap_analysis(data, selected_lap):

#     if not data or not selected_lap:
#         return go.Figure(), {"display": "none"}

#     race = data["race"]
#     driver = data["vehicle"]

#     # ---- Correct dynamic lap file ----
#     csv_path = (
#         f"../../../telemetry_split/{race}/driver_{driver}/lap_{selected_lap}.csv"
#     )
#     print(csv_path)

#     try:
#         df = pd.read_csv(csv_path)
#     except FileNotFoundError:
#         # No data for this lap
#         return go.Figure(), {"display": "none"}

#     # ---- Clean columns ----
#     df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
#     df["telemetry_value"] = pd.to_numeric(df["telemetry_value"], errors="coerce")

#     print(df.head())
#     print(df)

#     # ---- Filter Speed channel ----
#     df_speed = df[df["telemetry_name"].str.lower() == "speed"]
#     if df_speed.empty:
#         return go.Figure(), {"display": "none"}

#     # ---- Build final figure ----
#     fig = make_figure(df_speed, "telemetry_value", f"Speed — Lap {selected_lap}")

#     return fig, {"display": "block"}


# # ============================================================
# # DRIVER INFO CALLBACK
# # ============================================================
# @callback(
#     Output("driver_number", "children"),
#     Output("driver_name", "children"),
#     Output("driver_position", "children"),
#     Output("driver_status", "children"),
#     Output("driver_vehicle", "children"),
#     Output("driver_team", "children"),
#     Output("driver_laps", "children"),
#     Output("driver_country", "children"),
#     Input("session-store", "data")
# )
# def update_driver_info(data):

#     if not data:
#         return [""] * 8

#     csv_path = f"../../Datasets/indianapolis/{data['race']}/03_results.CSV"
#     df = pd.read_csv(csv_path, sep=";")

#     row = df[df["NUMBER"] == int(data["vehicle"])].iloc[0]

#     return (
#         row["NUMBER"],
#         f"{row['DRIVER_FIRSTNAME']} {row['DRIVER_SECONDNAME']}",
#         row["POSITION"],
#         row["STATUS"],
#         row["VEHICLE"],
#         row["TEAM"],
#         row["LAPS"],
#         row["DRIVER_COUNTRY"],
#     )

from dash import html, dcc, register_page, Output, Input, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import os

from components.search import search

register_page(__name__, path="/lap-analysis")


# ============================================================
# PAGE LAYOUT
# ============================================================
layout = dbc.Container([

    search,
    dcc.Store(id="session-store"),

    html.Br(),
    html.H6("Select Lap"),

    dcc.Slider(
        min=1, max=23, step=1, id="lap_slider",
        marks=None,
        tooltip={"placement": "bottom", "always_visible": True,
                 "style": {"color": "white", "fontSize": "10px"}}
    ),

    html.Br(),

    html.H6("Select Telemetry Channel(s)"),
    dcc.Dropdown(
        id="telemetry_filter",
        multi=True,
        placeholder="Choose telemetry channels (e.g., speed, aps, gear)..."
    ),

    html.Hr(),

    dcc.Graph(id="lap_graph", style={"height": "700px"}),

], fluid=True)


# ============================================================
# UPDATE GRAPH
# ============================================================
@callback(
    Output("telemetry_filter", "options"),
    Output("lap_graph", "figure"),
    Input("session-store", "data"),
    Input("lap_slider", "value"),
    Input("telemetry_filter", "value")
)
def update_lap_graph(data, lap, selected_channels):

    empty_fig = go.Figure()

    # No session or no lap: nothing to show
    if not data or lap is None:
        return [], empty_fig

    race = data.get("race")
    driver = data.get("vehicle")

    if not race or not driver:
        return [], empty_fig

    # ============================================================
    # DYNAMIC CSV PATH USING driver_{driver}
    # ============================================================

    csv_path = f"../../telemetry_split/{race}/driver_{driver}/lap_{lap}.csv"

    print("🔍 Loading CSV:", csv_path)

    if not os.path.exists(csv_path):
        print("CSV not found:", csv_path)
        return [], empty_fig

    # Load CSV
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print("Error loading CSV:", e)
        return [], empty_fig

    # Ensure correct types
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["telemetry_value"] = pd.to_numeric(df["telemetry_value"], errors="coerce")

    # All unique telemetry channels
    telemetry_options = sorted(df["telemetry_name"].unique())

    # If none selected yet, default to all
    if not selected_channels or len(selected_channels) == 0:
        selected_channels = telemetry_options

    # ============================================================
    # BUILD WEBGL GRAPH
    # ============================================================
    fig = go.Figure()

    for channel in selected_channels:
        channel_df = df[df["telemetry_name"] == channel]

        fig.add_trace(go.Scattergl(
            x=channel_df["timestamp"],
            y=channel_df["telemetry_value"],
            mode="lines",
            name=channel,
            hovertemplate="Time: %{x}<br>Value: %{y}<extra></extra>"
        ))

    fig.update_layout(
        template="plotly_dark",
        title=f"Lap {lap} — Driver {driver} — Telemetry",
        xaxis_title="Timestamp",
        yaxis_title="Telemetry Value",
        height=700,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(font=dict(size=10))
    )

    return telemetry_options, fig
# /Users/oluwasojilasaki/Downloads/Hackathon/telemetry_split/Race 1/driver_0

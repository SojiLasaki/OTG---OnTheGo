from dash import html, dcc, register_page, Output, Input, State, callback
import dash_bootstrap_components as dbc
import requests
from components.search import search

register_page(__name__, path="/compare")

layout = dbc.Container([
    search,
    dcc.Store(id="session-store"),

    html.H4("Compare Drivers", style={"textAlign": "center", "marginTop": "20px", "marginBottom": "20px"}),

    # ---------------- COMPARISON TYPE ----------------
    dbc.Row([
        dbc.Col([
            dbc.RadioItems(
                id="compare_type_radio",
                options=[
                    {"label": "Compare to Best Lap", "value": "best"},
                    {"label": "Compare to Another Driver", "value": "driver"}
                ],
                value="best",
                inline=True
            )
        ], width=12)
    ],style={ "textAlign": "center", "marginTop": "20px", "marginBottom": "20px" }),

    # ---------------- DRIVER 2 DROPDOWN ----------------
    dbc.Row([
        dbc.Col([
            html.Label("Select Driver to Compare:", style={"marginBottom":"20px"}),
            dcc.Dropdown(
                id="driver2_dropdown",
                placeholder="Select driver"
            )
        ], width=6, className="mx-auto", style={ "textAlign": "center", "marginTop": "20px","marginBottom": "20px" })
    ], id="driver2_row"),

    # ---------------- BUTTON ----------------
    dbc.Row([
        dbc.Col([
            dbc.Button("Compare", id="compare_btn", color="primary")
        ], width="auto")
    ], justify="center", style={"marginBottom": "20px"}),

    html.Hr(),

    # ---------------- OUTPUT ----------------
    html.Div(id="comparison_output", style={"whiteSpace": "pre-line", "color": "white"})
], fluid=True)

# ============================================================
# SHOW/HIDE DRIVER 2 AND POPULATE DROPDOWN
# ============================================================
@callback(
    Output("driver2_row", "style"),
    Output("driver2_dropdown", "options"),
    Input("compare_type_radio", "value"),
    State("session-store", "data")
)
def toggle_driver2(compare_type, session):
    if compare_type != "driver":
        return {"display": "none"}, []
    
    # Fetch available drivers from session (excluding current driver)
    driver1 = session.get("vehicle") if session else None
    all_drivers = session.get("all_drivers", []) if session else []
    options = [{"label": d, "value": d} for d in all_drivers if d != driver1]
    
    return {"display": "block", "marginBottom": "20px"}, options

# ============================================================
# COMPARE DRIVERS
# ============================================================
@callback(
    Output("comparison_output", "children"),
    Input("compare_btn", "n_clicks"),
    State("compare_type_radio", "value"),
    State("driver2_dropdown", "value"),
    State("session-store", "data")
)
def compare_drivers(n_clicks, compare_type, driver2, session):
    if not n_clicks:
        return "Enter drivers to compare."
    if not session:
        return "No session data loaded."

    driver1 = session.get("vehicle")
    race = session.get("race")
    lap = session.get("lap", 1)  # fetch lap from session

    if not driver1:
        return "Driver 1 is required."
    if compare_type == "driver" and not driver2:
        return "Driver 2 is required for this comparison."

    payload = {"race": race, "driver": driver1, "lap": lap, "compare_type": compare_type}
    if compare_type == "driver":
        payload["other_driver"] = driver2
        payload["other_lap"] = lap

    try:
        response = requests.post("http://127.0.0.1:5000/compare", json=payload)
        response.raise_for_status()
        result = response.json()
        if compare_type == "driver":
            return f"Driver {driver1} Lap {lap} vs Driver {driver2} Lap {lap}:\n\n{result.get('analysis', '')}"
        else:
            return f"Driver {driver1} Lap {lap} vs Best Lap:\n\n{result.get('analysis', '')}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to backend: {str(e)}"

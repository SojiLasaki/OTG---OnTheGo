import dash
from dash import Input, Output, State, page_container, dcc, html, dash_table
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.search import search
import os
from dash.exceptions import PreventUpdate
import pandas as pd
# from assests.urls import CSV_URLS
import requests

# Global session store (for debugging or reference)
session_data = {}

BASE_DIR = os.path.dirname(os.getcwd())

# --- Load datasets ---
datasets = "../../Datasets/indianapolis/"


# --- Initialize Dash app ---
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True
)
app.title = "On The GO"
server = app.server


# --- App Layout ---
app.layout = dbc.Container([
    dcc.Store(id="session-store", storage_type="session"),
    navbar,
    dash.page_container,
], fluid=True)


# --- Navbar Collapse ---
@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
)
def toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


# --- Update Race Dropdown ---
# @app.callback(
#     Output("race-dropdown", "options"),
#     Input("map-dropdown", "value")
# )
# def update_races(selected_map):
#     if not selected_map:
#         return ["No races found"]

#     map_path = os.path.join(datasets, selected_map)
#     races = [f for f in os.listdir(map_path) if not f.startswith(".")]
#     races_sorted = sorted(races, key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
#     return [{"label": f.title(), "value": f} for f in races_sorted]


# --- Update Vehicle Dropdown ---
@app.callback(
    Output("vehicle-dropdown", "options"),
    Input("race-dropdown", "value")
)
def update_vehicle(selected_race):
    if not selected_race:
        return []

    race_path = os.path.join(datasets, selected_race)
    print(f"Reading vehicle list from: {race_path}")

    try:
        df = pd.read_csv(f"{race_path}/03_results.CSV", sep=";")
        if "NUMBER" not in df.columns:
            return [{"label": "No Vehicles Found", "value": ""}]

        numbers = sorted(df["NUMBER"].unique())
        return [{"label": str(num), "value": str(num)} for num in numbers]

    except FileNotFoundError:
        return [{"label": "File not found", "value": ""}]
    except Exception as e:
        return [{"label": f"Error: {e}", "value": ""}]


# --- Save Session Data ---
@app.callback(
    Output("session-store", "data"),
    Input("search-btn", "n_clicks"),
    State("race-dropdown", "value"),
    State("vehicle-dropdown", "value"),
    prevent_initial_call=True
)
def save_to_session(n_clicks, selected_race, selected_vehicle):
    if not selected_race or not selected_vehicle:
        raise PreventUpdate

    data = {
        "race": selected_race,
        "vehicle": selected_vehicle
    }

    global session_data
    session_data = data  # optional (for debugging)
    print("Session saved:", session_data)
    return data


# --- Show Session on Other Pages ---
@app.callback(
    Output("other-page-output", "children"),
    Input("session-store", "data")
)
def show_session_data(data):
    if not data:
        return "No data in session yet."
    return f"Map: {data['map']}, Race: {data['race']}, Vehicle: {data['vehicle']}"

    # return summary, table

# --- Overview Table ---
@app.callback(
    Output("overview-summary", "children"),
    Output("overview-table", "children"),
    Input("session-store", "data"),
    prevent_initial_call=True
)
def update_overview(session_data):
    if not session_data:
        return html.P("⚠️ No session data found. Please select a race first."), None

    selected_map = session_data.get("map")
    selected_race = session_data.get("race")
    selected_vehicle = session_data.get("vehicle")

    root = "../../"
    file_path = f"{root}Datasets/indianapolis/{selected_race}/03_results.CSV"

    if not os.path.exists(file_path):
        return html.P(f"File not found: {file_path}"), None

    df = pd.read_csv(file_path, sep=";")

    summary = html.Div([
        html.H5(f"{selected_race}", className="text-center mb-2"),
        html.P(f"Total Vehicles: {len(df)}", className="text-center")
    ])

    # Highlight vehicle row
    highlight_style = []
    if selected_vehicle and "Vehicle" in df.columns:
        highlight_style.append({
            "if": {"filter_query": f"{{Vehicle}} = '{selected_vehicle}'"},
            "backgroundColor": "#FFD700",
            "color": "black",
            "fontWeight": "bold",
        })

    # DataTable
    table = dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=100,
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "center",
            "backgroundColor": "#111",
            "color": "white",
        },
        style_header={
            "backgroundColor": "#5c5c5c",
            "fontWeight": "bold",
        },
        style_data_conditional=highlight_style
    )

    return summary, table


# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)

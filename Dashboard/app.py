import dash
from dash import Input, Output, State, page_container, dcc, html, dash_table
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.search import search
import os
from dash.exceptions import PreventUpdate
import pandas as pd

session_data = {}

datasets = "../../Datasets/indianapolis/"

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True
)
app.title = "On The GO"
server = app.server

app.layout = dbc.Container([
    dcc.Store(id="session-store", storage_type="session"),
    navbar,
    dash.page_container,
], fluid=True)

@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
)
def toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output("vehicle-dropdown", "options"),
    Input("race-dropdown", "value")
)
def update_vehicle(selected_race):
    if not selected_race:
        return []

    race_path = os.path.join(datasets, selected_race)

    try:
        df = pd.read_csv(f"{race_path}/03_results.CSV", sep=";")
        if "NUMBER" not in df.columns:
            return [{"label": "No Vehicles Found", "value": ""}]

        numbers = sorted(df["NUMBER"].unique())
        return [{"label": str(num), "value": str(num)} for num in numbers]

    except:
        return [{"label": "Error loading file", "value": ""}]

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

    return data

@app.callback(
    Output("overview-summary", "children"),
    Output("overview-table", "children"),
    Input("session-store", "data"),
    prevent_initial_call=True
)
def update_overview(session_data):
    if not session_data:
        return html.P("⚠️ No session data."), None

    selected_race = session_data["race"]
    selected_vehicle = session_data["vehicle"]

    file_path = f"../../Datasets/indianapolis/{selected_race}/03_results.CSV"

    if not os.path.exists(file_path):
        return html.P(f"File not found: {file_path}"), None

    df = pd.read_csv(file_path, sep=";")

    summary = html.Div([
        html.H5(f"{selected_race}", className="text-center mb-2"),
        html.P(f"Total Vehicles: {len(df)}", className="text-center")
    ])

    table = dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=100,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center", "backgroundColor": "#111", "color": "white"},
        style_header={"backgroundColor": "#5c5c5c", "fontWeight": "bold"}
    )

    return summary, table

if __name__ == "__main__":
    app.run(debug=True)

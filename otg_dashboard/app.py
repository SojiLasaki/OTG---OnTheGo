import dash
from dash import Input, Output, State, page_container, dcc
import dash_bootstrap_components as dbc
from components.navbar import navbar
from components.line import line


# initialize app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.CYBORG])
app.title = "On The GO"


# App layout
app.layout = dbc.Container([
    dcc.Store(id="selection_store", storage_type="session"),
    navbar,
    dash.page_container
], fluid=True)


# Callback to toggle collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
)

def toggle_navbar(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open


# run app
if __name__ == "__main__":
    app.run(debug=True)
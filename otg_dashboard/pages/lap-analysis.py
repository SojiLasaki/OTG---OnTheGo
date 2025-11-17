import dash_bootstrap_components as dbc
from dash import register_page, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import os
from dash import get_app
app = get_app()

# --- Reusable Function ---
def create_line_chart_from_csv(csv_path, x_col, y_col, title="Line Chart", color_col=None):
    """
    Create a reusable Plotly line chart from a CSV file.
    """
    if not os.path.exists(csv_path):
        return None  # handle missing file safely

    df = pd.read_csv(csv_path)
    fig = px.line(
        data_frame=df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        markers=True
    )
    fig.update_layout(
        template="plotly_white",
        title_font=dict(size=20, color="black"),
        xaxis_title=x_col.capitalize(),
        yaxis_title=y_col.capitalize(),
        hovermode="x unified",
        legend_title_text=color_col.capitalize() if color_col else "",
    )
    return fig


# --- Register Page ---
register_page(__name__, path="/lap-analysis")

# --- Layout ---
layout = dbc.Container([
    dcc.Store(id="session-store"),  # shared session data

    dbc.Row([
        dbc.Col([
            html.H5("Lap Analysis Section", className="text-center text-white"),
            html.Hr()
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.H4('Lap Time Visualization', className='text-white'),
            dcc.Graph(id="lap-line-chart")  # dynamically updated
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H1('Here is an example'),
            html.P("Image goes here")
        ]),
        dbc.Col([
            html.H1('Here is an example'),
            html.P("Image goes here")
        ]),
        dbc.Col([
            html.H1('Here is an example'),
            html.P("Image goes here")
        ])
    ])

], fluid=True, className="p-4 text-white")


# --- Callback to Load CSV and Display Chart ---
@app.callback(
    Output("lap-line-chart", "figure"),
    Input("session-store", "data")
)
def update_chart_from_session(session_data):
    if not session_data:
        # Return empty chart until session is set
        return px.line(title="No session data yet")

    selected_map = session_data.get("map")
    selected_race = session_data.get("race")

    csv_path = f"../Datasets/{selected_map}/{selected_race}/26_Weather_{selected_race}_Anonymized.csv"
    df = pd.read_csv(csv_path, sep=";")
    print(df)


    fig = create_line_chart_from_csv(
        csv_path=df,
        x_col="WIND_SPEED",
        y_col="TIME_UTC_STR",
        color_col="driver",
        title=f"Lap Time Analysis - {selected_map} ({selected_race})"
    )

    if fig is None:
        return px.line(title="CSV file not found or invalid.")

    return fig

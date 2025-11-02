from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load your weather dataset
# df = pd.read_csv("weather_data.csv", sep=';')
root = "../../../"
df = pd.read_csv(f'{root}Datasets/Road America/Race 1/26_Weather_Race 1_Anonymized.csv', sep=';')

# Initialize Dash app
app = Dash(__name__)
app.title = "Weather Dashboard"

# List of numeric columns for dropdown
numeric_cols = ['AIR_TEMP', 'TRACK_TEMP', 'HUMIDITY', 'PRESSURE', 'WIND_SPEED']

# Define app layout
app.layout = html.Div([
    html.H1("🌤️ Interactive Weather Dashboard", style={'textAlign': 'center'}),

    dcc.Tabs(id='tabs', value='tab1', children=[
        dcc.Tab(label='Wind Speed Analysis', value='tab1'),
        dcc.Tab(label='Temperature Analysis', value='tab2'),
        dcc.Tab(label='Humidity & Pressure', value='tab3'),
    ]),

    html.Div(id='tab-content')
])


# Define callback for changing tab content
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    if tab == 'tab1':
        return html.Div([
            html.H3("Wind Speed Comparison"),
            html.Label("Select variable to compare with Wind Speed:"),
            dcc.Dropdown(
                id='compare-dropdown',
                options=[{'label': col, 'value': col} for col in numeric_cols if col != 'WIND_SPEED'],
                value='AIR_TEMP'
            ),
            dcc.Graph(id='wind-graph')
        ])

    elif tab == 'tab2':
        return html.Div([
            html.H3("Temperature Trends"),
            dcc.RadioItems(
                id='temp-type',
                options=[
                    {'label': 'Air Temperature', 'value': 'AIR_TEMP'},
                    {'label': 'Track Temperature', 'value': 'TRACK_TEMP'}
                ],
                value='AIR_TEMP',
                inline=True
            ),
            dcc.Graph(id='temp-graph')
        ])

    elif tab == 'tab3':
        return html.Div([
            html.H3("Humidity and Pressure Over Time"),
            dcc.Graph(
                figure=px.line(df, x='TIME_UTC_STR', y=['HUMIDITY', 'PRESSURE'], title='Humidity & Pressure')
            )
        ])


# Callback for tab 1 — dynamic comparison plot
@app.callback(
    Output('wind-graph', 'figure'),
    Input('compare-dropdown', 'value')
)
def update_wind_graph(compare_col):
    fig = px.line(df, x='TIME_UTC_STR', y=['WIND_SPEED', compare_col],
                  title=f"Wind Speed vs {compare_col}",
                  markers=True)
    fig.update_layout(xaxis_title="Time (UTC)", yaxis_title="Value")
    return fig


# Callback for tab 2 — temperature selector
@app.callback(
    Output('temp-graph', 'figure'),
    Input('temp-type', 'value')
)
def update_temp_graph(temp_type):
    fig = px.line(df, x='TIME_UTC_STR', y=temp_type,
                  title=f"{temp_type} Over Time",
                  markers=True)
    fig.update_layout(xaxis_title="Time (UTC)", yaxis_title="Temperature (°C)")
    return fig


# Run app
if __name__ == '__main__':
    app.run(debug=True)

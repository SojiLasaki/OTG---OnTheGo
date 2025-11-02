import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import register_page, html

register_page(__name__, path="/overview")
layout = html.Div([
    html.H1("Welcome to OTG"),
    html.P("Select a race")
])
# load data
time = np.linspace(0,60,600)
root = "../"
df = pd.read_csv(f'{root}Datasets/Road America/Race 1/26_Weather_Race 1_Anonymized.csv', sep=';')
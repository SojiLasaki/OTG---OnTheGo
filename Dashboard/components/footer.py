from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

footer = dbc.Container([
        dbc.Row([
            html.Div(className="mt-3"),
            html.Hr(),
            dbc.Col([
                html.H6("On The Go was created by"),
                html.Div([
                        html.H6("Oluwasoji Lasaki", className="ms-2"),
                        html.H6("-"),
                        html.H6("Inioluwa Oyatobo"),
                        html.H6("-"),
                        html.H6("Nakshatra Bobilli"),
                        html.H6("-"),
                        html.H6("Hamza Tai"),
                    ],className="d-flex gap-4", 
                ),
                html.Hr(),
                html.H6("Indiana University Students"),
                html.H6('November 2025 - Hack The Track Hackathon')
            ])
        ]),
    ],
     className="d-flex justify-content-center align-items-center text-align-center", style={"margin":"auto", "textAlign":"center"}
)

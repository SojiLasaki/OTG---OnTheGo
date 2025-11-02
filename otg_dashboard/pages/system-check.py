from dash import html, register_page

register_page(__name__, path='/system-check')

layout = html.Div(
    html.H1("System Check")
)
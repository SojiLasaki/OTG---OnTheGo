from dash import html, register_page

register_page(__name__, path="/lap-analysis")

layout = html.Div(
    html.H1("Lap Analysis")
)
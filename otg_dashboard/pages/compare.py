from dash import html, register_page

register_page(__name__,path="/compare")

layout = html.Div([
    html.H1("Compare"),
    html.P("Select a race")
])
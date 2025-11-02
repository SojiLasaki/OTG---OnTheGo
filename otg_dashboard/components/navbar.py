import dash
from dash import html
import dash_bootstrap_components as dbc

# Navbar layout
navbar = dbc.Navbar(
    dbc.Container([

        # Brand text on the left
        dbc.NavbarBrand(
            html.H6("On The Go", className="mt-2 h6"),
            href="/",
        ),

        # Hamburger toggle for small screens
        dbc.NavbarToggler(id="navbar-toggler"),

        # Collapsible nav links (right-aligned)
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", className="ps-3 text-white"),
                    dbc.NavLink("Overview", href="/overview", className="ps-3 text-white"),
                    dbc.NavLink("Lap Analysis", href="/lap-analysis", className="ps-3 text-white"),
                    dbc.NavLink("System Check", href="/system-check", className="ps-3 text-white"),
                    dbc.NavLink("Compare", href="/compare", className="ps-3 text-white"),
                ],
                className="ms-auto d-flex align-items-center",
                navbar=True,
            ),
            id="navbar-collapse",
            is_open=False,
            navbar=True,
        ),
    ]),
    color="dark",
    dark=True,
    sticky="top",
    className="mt-2",
)

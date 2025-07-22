import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, html, dcc, Output, Input, State, no_update, MATCH, _dash_renderer
import pandas as pd
from datetime import date
import volunteerio.pages.login_page as login_page
import volunteerio.pages.hours_page as hours_page
import volunteerio.pages.about_page as about_page
import volunteerio.pages.admin_page as admin_page
from volunteerio.callbacks import login_callbacks, hours_callbacks, admin_callbacks
from volunteerio.server import create_app

app, server = create_app()

login_callbacks.register_login_callbacks(app)
hours_callbacks.register_callbacks(app)
admin_callbacks.register_callbacks(app)


_dash_renderer._set_react_version("18.2.0")

navbar = dbc.Navbar(
    id="navbar",
    children=[
        # dbc.NavbarBrand("EV Metrix", className="ms-5"),
        dbc.Nav(
            [
                dbc.NavItem(
                    dbc.NavLink(
                        "Home",
                        href="/",
                    ),
                ),
                dbc.NavItem(
                    dbc.NavLink("About", href="/about"),
                ),
                dbc.NavItem(dbc.NavLink("Admin", href="/admin")),
            ],
            pills=True,
        ),
    ],
    color="dark",
    dark=True,
    className="navbar-expand-lg bg-primary",
    style={"min-height": "70px"},
)
app.layout = dmc.MantineProvider(
    html.Div(
        [
            dcc.Location(id="url", refresh=False, pathname="/login"),
            navbar,
            dbc.Container(
                id="page-content",
                children=[login_page.layout],
                fluid=True,
                style={
                    "maxHeight": "calc(100vh - 70px)",
                    "overflowY": "hidden",
                },
            ),
            dcc.Store(id="user-store", data=""),
            dcc.Store(id="selected-date-store", data=date.today().isoformat()),
            dcc.Download(id="export-download"),
        ]
    )
)


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    # State("user-store", "data"),
    prevent_initial_call=True,
)
def display_page(pathname: str):  # , user: str):

    # if not user:
    #     return login_page.layout
    if pathname == "/":
        return login_page.layout
    elif pathname == "/hours":
        return hours_page.layout
    elif pathname == "/about":
        return about_page.layout
    elif pathname == "/admin":
        return admin_page.layout

    else:
        return "404 page not found"

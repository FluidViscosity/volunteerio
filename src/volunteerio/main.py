import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Dash, html, dcc, Output, Input, State, no_update, MATCH, _dash_renderer
import pandas as pd

import volunteerio.pages.login_page as login_page
import volunteerio.pages.hours_page as hours_page
from volunteerio.callbacks import login_callbacks, hours_callbacks
from volunteerio.server import create_app

app, server = create_app()

login_callbacks.register_login_callbacks(app)
hours_callbacks.register_callbacks(app)

_dash_renderer._set_react_version("18.2.0")

app.layout = dmc.MantineProvider(
    html.Div(
        [
            dcc.Location(id="url", refresh=False, pathname="/login"),
            dbc.Container(id="page-content", children=[login_page.layout], fluid=True),
            dcc.Store(id="user-store", data=""),
        ]
    )
)


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
    State("user-store", "data"),
    prevent_initial_call=True,
)
def display_page(pathname: str, user: str):

    if not user:
        return login_page.layout
    elif pathname == "/":
        return login_page.layout

    elif pathname == "/hours":
        return hours_page.layout
    else:
        return "404 page not found"

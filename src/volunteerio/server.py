from flask import Flask

from dash_extensions.enrich import DashProxy, ServersideOutputTransform

import dash_bootstrap_components as dbc


def create_app():
    server = Flask("VolunteerIO")
    app = DashProxy(
        __name__,
        server=server,
        external_stylesheets=[dbc.themes.SOLAR],
        transforms=[ServersideOutputTransform()],
        # suppress_callback_exceptions=True,
        title="VolunteerIO",
    )
    return app, server

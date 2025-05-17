from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
from dash_extensions.enrich import DashProxy, ServersideOutputTransform

import dash_bootstrap_components as dbc

# from db_config import design_info_modelling_db_url
# from data_intelligence_platform.extensions import db


def create_app():
    server = Flask("VolunteerIO")
    # server.config["SQLALCHEMY_DATABASE_URI"] = design_info_modelling_db_url
    # server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # db.init_app(server)

    app = DashProxy(
        __name__,
        server=server,
        external_stylesheets=[dbc.themes.SOLAR],
        transforms=[ServersideOutputTransform()],
        # suppress_callback_exceptions=True,
    )
    # with server.app_context():
    #     db.create_all()

    return app, server

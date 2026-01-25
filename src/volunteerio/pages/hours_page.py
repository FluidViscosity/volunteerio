from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from datetime import date

layout = dbc.Container(
    id="hours-root",
    fluid=True,  # This makes it full width
)

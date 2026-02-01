import dash_bootstrap_components as dbc
from dash import html, dcc
from datetime import date

import pandas as pd

layout = dbc.Container(
    [
        html.Br(),
        html.Div(
            html.H1("Admin"),
            style={"marginBottom": "20px"},
        ),
        dbc.Row(html.H2("Export Data")),
        dbc.Row(
            html.P(
                "Please export volunteer data for the period you are interested in. You may choose to export raw data or a summary of volunteer hours and activities."
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Export",
                    id="open-export-modal",
                ),
                width=2,
                align="center",
            )
        ),
        html.Br(),
        dbc.Row(
            html.H2("Users"),
        ),
        dbc.Row(
            html.P(
                "New users are to be added by park rangers or administrators only. For deletions contact the site administrator."
            ),
        ),
        dbc.Row(
            dbc.Col(
                [
                    dbc.Button("New user", id="new-user-modal-button", n_clicks=0),
                ],
                width=2,
                align="center",
            )
        ),
        dbc.Modal(
            id="new-user-modal",
            children=[
                dbc.ModalHeader("Add new user"),
                dbc.ModalBody(
                    children=[
                        dbc.Input(id="new-user-input"),
                        dcc.Dropdown(
                            id="new-user-team-input",
                            options=[
                                {"label": "Team1", "value": "Team1"},
                                {"label": "Team2", "value": "Team2"},
                            ],
                        ),
                        html.Div(id="new-user-error", className="text-danger"),
                        dbc.Button("Add", color="primary", id="new-user-button"),
                    ]
                ),
            ],
            is_open=False,
        ),
        dbc.Modal(
            id="export-modal",
            children=[
                dbc.ModalHeader("Export"),
                dbc.ModalBody(
                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.DatePickerRange(
                                    id="export-dates",
                                    min_date_allowed="2025-01-01",
                                    max_date_allowed=date.today(),
                                    minimum_nights=0,
                                    start_date=date.today()
                                    - pd.tseries.offsets.MonthBegin(2),
                                ),
                                width=6,
                            ),
                            dbc.Col(
                                [
                                    dbc.Checkbox(
                                        id="export-include-inactive-users-check",
                                        label="Include inactive users",
                                        value=False,
                                    ),
                                    dbc.Button(
                                        "Export Raw Data",
                                        id="export-modal-button",
                                        style={"margin-bottom": "8px"},
                                    ),
                                    dbc.Button(
                                        "Export Summary",
                                        id="export-activity-summary-button",
                                        style={"margin-bottom": "8px"},
                                    ),
                                ],
                                width=6,
                                # class_name="m-2",
                            ),
                        ]
                    )
                ),
            ],
            size="lg",
        ),
    ],
)

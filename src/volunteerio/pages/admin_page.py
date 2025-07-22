import dash_bootstrap_components as dbc
from dash import html, dcc
from datetime import date

layout = dbc.Container(
    [
        html.Br(),
        html.Div(
            html.H1("Admin"),
            style={"marginBottom": "20px"},
        ),
        dbc.Row(
            [
                # dbc.Input(id="new-user-input", placeholder="New user"),
                dbc.Button("New user", id="new-user-modal-button", n_clicks=0),
            ]
        ),
        html.Br(),
        dbc.Row(
            dbc.Button(
                "Export all",
                id="open-export-modal",
            )
        ),
        dbc.Modal(
            id="new-user-modal",
            children=[
                dbc.ModalHeader("Add new user"),
                dbc.ModalBody(
                    children=[
                        dbc.Input(id="new-user-input"),
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
                                ),
                                width=8,
                            ),
                            dbc.Col(
                                dbc.Button("Export", id="export-modal-button"),
                                width=4,
                            ),
                        ]
                    )
                ),
            ],
        ),
    ],
)

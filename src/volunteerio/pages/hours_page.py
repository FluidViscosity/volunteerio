from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from datetime import date

layout = dbc.Container(
    [
        dbc.Row(dbc.Col(id="hours-user-title", children=[])),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(dbc.Button("<", id="calendar-previous-button"), width=1),
                dbc.Col(
                    dbc.Button(">", id="calendar-next-button"),
                    width=1,
                    class_name="text-end",
                ),
            ],
            justify="between",
        ),
        html.Br(),
        dbc.Row(dbc.Col(id="hours-table-col")),
        html.Br(),
        dbc.Row(dbc.Col(dbc.Button("Export", id="open-export-modal"))),
        dbc.Modal(
            id="export-modal",
            children=[
                dbc.ModalHeader("Export"),
                dbc.ModalBody(
                    dbc.Row(
                        dbc.Col(
                            [
                                dcc.DatePickerRange(
                                    id="export-dates",
                                    min_date_allowed="2025-01-01",
                                    max_date_allowed=date.today(),
                                    minimum_nights=0,
                                ),
                                dbc.Button("Export", id="export-modal-button"),
                            ]
                        )
                    )
                ),
            ],
        ),
        html.P(id="cell-changed", style={"display": "None"}),
    ],
    # className="d-flex flex-column align-items-center justify-content-center vh-100",
)

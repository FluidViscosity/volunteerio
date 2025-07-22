from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from datetime import date

layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Col(  # user card column
                    dbc.Row(
                        [
                            dbc.Card(
                                [
                                    dbc.CardHeader(id="hours-user-title"),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(id="hours-card-body"),
                                        ]
                                    ),
                                    dbc.NavLink(
                                        dbc.Button("Save"),
                                        id="save-button",
                                        href="/",
                                    ),
                                ],
                            )
                        ]
                    ),
                    style={"padding-top": "40px"},
                    width=2,
                ),
                dbc.Col(  # data column
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("<", id="calendar-previous-button"),
                                    width=1,
                                ),
                                dbc.Col(
                                    html.H3(id="month-label"),
                                    class_name="text-center",
                                    width=10,
                                ),
                                dbc.Col(
                                    dbc.Button(">", id="calendar-next-button"),
                                    width=1,
                                    class_name="text-end",
                                ),
                            ],
                            justify="between",
                        ),
                        dbc.Row(dbc.Col(id="hours-table-col")),
                    ],
                    width=10,
                ),
            ]
        ),
        # dbc.Row(dbc.Col(id="hours-user-title", children=[])),
        # html.Br(),
        html.P(id="cell-changed", style={"display": "None"}),
    ],
    fluid=True,  # This makes it full width
    # className="d-flex flex-column align-items-center justify-content-center vh-100",
)

from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H1("Shakespear Regional Park", style={"textAlign": "center"}),
                    html.H3("Volunteer Hour Logging", style={"textAlign": "center"}),
                ],
                width=12,
            )
        ),
        html.Br(),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    dcc.Dropdown(
                                        id="username-input",
                                        placeholder="Username",
                                        style={"min-width": "120px"},
                                        # options=["Name1", "Name2", "Add new..."],
                                    ),
                                ),
                                html.Br(),
                                dbc.Row(
                                    dbc.Button(
                                        "Log hours",
                                        id="login-button",
                                        color="primary",
                                        style={"min-width": "120px"},
                                        n_clicks=0,
                                    ),
                                    justify="center",
                                ),
                            ],
                            width=4,
                        ),
                    ],
                    justify="center",
                ),
                # dbc.Row(
                #     dbc.Col(
                #         align="center",
                #     ),
                #     justify="center",
                #     className="d-grid gap-2 col-4 mx-auto",
                # ),
            ],
            # className="w-100",
        ),
    ],
    className="d-flex flex-column align-items-center justify-content-center vh-100",
)

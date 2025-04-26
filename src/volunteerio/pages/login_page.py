from dash import html, dcc
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("VolunteerIO", style={"textAlign": "center"}),
                width=12,
            )
        ),
        html.Br(),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                id="username-input",
                                placeholder="Username",
                                # options=["Name1", "Name2", "Add new..."],
                            ),
                            width=4,
                        ),
                    ],
                    justify="center",
                ),
                html.Br(),
                dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            "Login", id="login-button", color="primary", n_clicks=0
                        ),
                        width=4,
                        align="center",
                    ),
                    justify="center",
                    className="d-grid gap-2 col-4 mx-auto",
                ),
                dbc.Modal(
                    id="new-user-modal",
                    children=[
                        dbc.ModalHeader("Add new user"),
                        dbc.ModalBody(
                            children=[
                                dbc.Input(id="new-user-input"),
                                dbc.Button(
                                    "Add", color="primary", id="new-user-button"
                                ),
                            ]
                        ),
                    ],
                    is_open=False,
                ),
            ],
            className="w-100",
        ),
    ],
    className="d-flex flex-column align-items-center justify-content-center vh-100",
)

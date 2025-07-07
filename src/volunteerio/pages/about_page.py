import dash_bootstrap_components as dbc
from dash import html

layout = dbc.Container(
    [
        html.Br(),
        html.Div(
            html.H1("About"),
            style={"marginBottom": "20px"},
        ),
        html.Div(
            html.P(
                """VolunteerIO is a website to help volunteers log their hours and activities at Shakespear Regional Park. \nCreated by a park volunteer and the team at Shakespear Regional Park. Do reach out to us if you have any questions or suggestions.""",
            ),
            style={"marginBottom": "20px", "whiteSpace": "pre-wrap"},
        ),
        html.Div(
            html.H3("Data"),
            style={"marginBottom": "20px"},
        ),
        html.Div(
            [
                html.P(
                    "Only a name is required for the website, which will be accessible by anyone at this website. Your data will never be sold."
                ),
            ],
        ),
        html.Div(
            html.H3("Contact Us"),
            style={"marginBottom": "20px"},
        ),
        html.Div(
            [
                html.P("Email: info@sossi.org.nz"),
            ],
        ),
    ],
)

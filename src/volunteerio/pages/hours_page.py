from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

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
        dbc.Row(dbc.Col(dash_table.DataTable(id="calendar-table", editable=True))),
        html.Br(),
        # dbc.Row(
        #     dbc.Col(
        #         dcc.Dropdown(
        #             id="add-activity-dropdown",
        #             multi=False,
        #             options=["activity1", "activity2", "activity3"],
        #             clearable=True,
        #             searchable=True,
        #             placeholder="Add activity",
        #         ),
        #         width=4,
        #     )
        # ),
    ],
    # className="d-flex flex-column align-items-center justify-content-center vh-100",
)

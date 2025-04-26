from copy import deepcopy
from dash import html, Input, Output, State, no_update, dash_table, callback_context
from volunteerio.db_config import db_params
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import psycopg2
from datetime import date, timedelta


def get_week_dates(selected_date: str):
    # weekday 0 = Monday
    selected_date = date.fromisoformat(selected_date)
    weekday = selected_date.weekday()
    # create an array of dates, Monday-Sunday including the current date.
    week = []
    for i in range(weekday):
        week.append(selected_date - timedelta(days=weekday - i))
    for i in range(7 - weekday):
        week.append(selected_date + timedelta(days=i))

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    return [f"{res[0]} {res[1].day}" for res in zip(days, week)], week


def get_hours(user: str, selected_date: str) -> tuple[list[str], list[tuple]]:
    day_titles, dates = get_week_dates(selected_date)

    sum_cases = []
    for d in dates:
        colname = d.isoformat()
        sum_case = f"""
            SUM(
                CASE 
                    WHEN store.date = %s AND v.name = %s THEN store.hours
                    ELSE 0
                END
            ) AS "{colname}"
            """
        sum_cases.append(sum_case)

    sum_cases_sql = ",\n    ".join(sum_cases)

    query = f"""
        SELECT
            a.activity,
            {sum_cases_sql}
        FROM
            activities a
        LEFT JOIN activity_store store ON store.activity_id = a.id
        LEFT JOIN volunteers v ON v.id = store.volunteer_id
        GROUP BY
            a.activity
        ORDER BY
            a.activity;
    """

    query_params = []
    for d in dates:
        query_params.append(d.isoformat())  # store.date = ?
        query_params.append(user)  # v.name = ?

    with psycopg2.connect(**db_params) as con:
        with con.cursor() as cur:
            cur.execute(query, query_params)
            res = cur.fetchall()

    return day_titles, res


def create_calendar(user: str, date: str) -> html.Table:

    days, display_hours = get_hours(user, date)
    cols = ["Activity"] + days
    # convert display hours to a list of dictionaries
    data = []
    for i in range(len(display_hours)):
        data.append(
            {
                z[0]: z[1].title() if isinstance(z[1], str) else float(z[1])
                for z in zip(cols, display_hours[i])
            }
        )

    return cols, data


def register_callbacks(app) -> None:
    @app.callback(
        Output("hours-user-title", "children"),
        Output("hours-table-col", "children"),
        # Output("calendar-table", "columns", allow_duplicate=True),
        # Output("calendar-table", "data", allow_duplicate=True),
        Input("url", "pathname"),
        Input("selected-date-store", "data"),
        State("user-store", "data"),
    )
    def prepare_hours_page(url: str, cur_date: str, user: str):
        if url != "/hours":
            return no_update

        cols, data = create_calendar(user, cur_date)
        table = (
            dag.AgGrid(
                id="basic-editing-example",
                columnDefs=[{"field": i} for i in cols],
                rowData=data,
                columnSize="sizeToFit",
                defaultColDef={"editable": True, "cellDataType": False},
                dashGridOptions={"animateRows": False},
            ),
        )

        return html.H1(user, style={"textAlign": "center"}), table

    @app.callback(
        Output("selected-date-store", "data"),
        Input("calendar-previous-button", "n_clicks"),
        Input("calendar-next-button", "n_clicks"),
        State("selected-date-store", "data"),
    )
    def update_date(
        prev_clicks: int | None, next_clicks: int | None, cur_date: str
    ) -> str:
        if prev_clicks is None and next_clicks is None:
            return no_update
        button = callback_context.triggered_id
        if button == "calendar-previous-button":
            new_date = date.fromisoformat(cur_date) - timedelta(days=7)
        else:
            new_date = date.fromisoformat(cur_date) + timedelta(days=7)

        return new_date.isoformat()


# https://github.com/MatthieuRu/run-together/blob/main/dash_apps/run_together/components/calendar_training.py
# https://pip-install-python.com/pip/full_calendar_component
# https://medium.com/@matthieu.ru/5f285bc7de9b

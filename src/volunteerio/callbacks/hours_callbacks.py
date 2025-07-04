from copy import deepcopy
from dash import (
    html,
    Input,
    Output,
    State,
    no_update,
    dash_table,
    callback_context,
    dcc,
)
from dash.exceptions import PreventUpdate
import pandas as pd
from volunteerio.db_config import db_params
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import psycopg2
from datetime import date, datetime, timedelta


def get_week_dates(selected_date: str):
    # weekday 0 = Monday
    selected_datetime = date.fromisoformat(selected_date)
    weekday = selected_datetime.weekday()
    # create an array of dates, Monday-Sunday including the current date.
    week = []
    for i in range(weekday):
        week.append(selected_datetime - timedelta(days=weekday - i))
    for i in range(7 - weekday):
        week.append(selected_datetime + timedelta(days=i))

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

    with psycopg2.connect(**db_params) as con:  # type: ignore
        with con.cursor() as cur:
            cur.execute(query, query_params)
            res = cur.fetchall()

    return day_titles, res


def get_date_from_col(current_date: str, col_id: str):
    cur_date = date.fromisoformat(current_date)
    weekday = cur_date.weekday()
    for i in range(weekday + 1):
        d = cur_date - timedelta(days=i)
        if d.day == int(col_id.split(" ")[1]):
            return d
    for i in range(7 - weekday):
        d = cur_date + timedelta(days=i)
        if d.day == int(col_id.split(" ")[1]):
            return d


def create_calendar(user: str, date: str) -> tuple[list[str], list[dict]]:

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
        Output("month-label", "children"),
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
                id="hours-table",
                columnDefs=[
                    (
                        {"field": i, "editable": False, "flex": 1}
                        if "activity" in i.lower()
                        else {
                            "field": i,
                            "editable": True,
                            "cellDataType": "number",
                            "flex": 1,
                        }
                    )
                    for i in cols
                ],
                rowData=data,
                columnSize="sizeToFit",
                dashGridOptions={
                    "animateRows": False,
                },
            ),
        )
        date = datetime.fromisoformat(cur_date)
        month = date.strftime("%B")

        return html.H1(user, style={"textAlign": "center"}), table, month

    @app.callback(
        Output("cell-changed", "children"),
        Input("hours-table", "cellValueChanged"),
        State("selected-date-store", "data"),
        State("user-store", "data"),
    )
    def update_hours(cell_changed: dict, cur_date: str, volunteer_name: str) -> str:
        if cell_changed is None:
            return no_update
        hours = float(cell_changed[0]["value"])
        activity = cell_changed[0]["data"]["Activity"].lower()
        set_date = get_date_from_col(
            current_date=cur_date, col_id=str(cell_changed[0]["colId"])
        )
        with psycopg2.connect(**db_params) as con:  # type: ignore
            with con.cursor() as cur:
                query = """
                WITH v AS (
                    SELECT id AS volunteer_id FROM volunteers WHERE name = %s
                ),
                a AS (
                    SELECT id AS activity_id FROM activities WHERE activity = %s
                )
                INSERT INTO activity_store (volunteer_id, activity_id, date, hours)
                SELECT v.volunteer_id, a.activity_id, %s, %s
                FROM v, a
                ON CONFLICT (volunteer_id, activity_id, date)
                DO UPDATE SET hours = EXCLUDED.hours;
                """

                cur.execute(query, (volunteer_name, activity, set_date, hours))

        return f"{cell_changed}"

    @app.callback(
        Output("selected-date-store", "data"),
        Input("calendar-previous-button", "n_clicks"),
        Input("calendar-next-button", "n_clicks"),
        State("selected-date-store", "data"),
    )
    def update_date(
        prev_clicks: int | None, next_clicks: int | None, cur_date: str
    ) -> str | PreventUpdate:
        if prev_clicks is None and next_clicks is None:
            raise PreventUpdate
        button = callback_context.triggered_id
        if button == "calendar-previous-button":
            new_date = date.fromisoformat(cur_date) - timedelta(days=7)
        else:
            new_date = date.fromisoformat(cur_date) + timedelta(days=7)

        return new_date.isoformat()

    @app.callback(
        Output("export-modal", "is_open"), Input("open-export-modal", "n_clicks")
    )
    def open_export_modal(n_clicks: int | None) -> bool:
        if n_clicks is None:
            raise PreventUpdate
        return True

    @app.callback(
        Output("export-download", "data"),
        Input("export-modal-button", "n_clicks"),
        State("export-dates", "start_date"),
        State("export-dates", "end_date"),
        State("user-store", "data"),
    )
    def export_data(n_clicks: int | None, start: str, end: str, user: str):
        if n_clicks is None:
            return no_update

        if start is None and end is None:
            return no_update

        with psycopg2.connect(**db_params) as con:  # type: ignore
            with con.cursor() as cur:
                query = """
                        SELECT store.id as record_id,
                        store.date as date,
                        v.id as volunteer_id,
                        v.name as volunteer_name,
                        a.activity as activity_name,
                        store.hours as hours
                        FROM activity_store store
                        LEFT JOIN volunteers v ON v.id = store.volunteer_id
                        LEFT JOIN activities a ON a.id = store.activity_id  
                        WHERE store.date BETWEEN %s AND %s
                        """
                df = pd.read_sql_query(query, con=con, params=(start, end))
        return dcc.send_data_frame(  # type: ignore
            df.to_csv, f"volunteerio_export_{start}_to_{end}.csv", index=False
        )


# https://github.com/MatthieuRu/run-together/blob/main/dash_apps/run_together/components/calendar_training.py
# https://pip-install-python.com/pip/full_calendar_component
# https://medium.com/@matthieu.ru/5f285bc7de9b

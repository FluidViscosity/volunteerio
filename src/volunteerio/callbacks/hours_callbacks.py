from copy import deepcopy
from dash import html, Input, Output, State, no_update, dash_table
import dash_bootstrap_components as dbc


def get_hours(activities: list[str], days: list[str]) -> list[dict]:
    data = []
    for act in activities:
        hours = {day.lower(): 0 for day in days}
        hours.update({"activity": act})
        data.append(hours)
    return data


def get_activities(user: str) -> list[str]:
    """
    Fetch the previous activities that the volunteer has undertaken from the database
    TODO
    """
    return ["Weeding", "Pest Control", "Planting"]


def create_calendar(user: str) -> html.Table:
    activities = get_activities(user)
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    display_hours = get_hours(activities, days)
    cols = ["Activity"] + days
    return [{"name": i, "id": i.lower()} for i in cols], display_hours


def register_callbacks(app) -> None:
    @app.callback(
        Output("hours-user-title", "children"),
        Output("calendar-table", "columns", allow_duplicate=True),
        Output("calendar-table", "data", allow_duplicate=True),
        Input("url", "pathname"),
        State("user-store", "data"),
    )
    def prepare_hours_page(url: str, user: str):
        if url != "/hours":
            return no_update

        cols, data = create_calendar(user)

        return html.H1(user, style={"textAlign": "center"}), cols, data

    @app.callback(
        Output("calendar-table", "data", allow_duplicate=True),
        Input("add-activity-dropdown", "value"),
        State("calendar-table", "data"),
        State("calendar-table", "columns"),
        prevent_initial_call=True,
    )
    def add_row(new_activity, rows, columns):
        if new_activity is None:
            return no_update

        new_row_data = {c["id"]: 0 for c in columns if c["id"] != "activity"}
        new_row_data.update({"activity": new_activity})

        rows.append(new_row_data)

        return rows


# https://github.com/MatthieuRu/run-together/blob/main/dash_apps/run_together/components/calendar_training.py
# https://pip-install-python.com/pip/full_calendar_component
# https://medium.com/@matthieu.ru/5f285bc7de9b

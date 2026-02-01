from dash import Output, Input, no_update, State
import pandas as pd
import psycopg2
from datetime import date

from volunteerio.db_config import db_params


def is_username_available(new_user: str) -> bool:
    with psycopg2.connect(**db_params) as con:  # type: ignore
        with con.cursor() as cur:
            query = """
                    SELECT v.name
                    FROM volunteers v;
                    """
            cur.execute(query)
            res = cur.fetchall()
            for user in res:
                if new_user.lower() == str(user[0]).lower():
                    return False

    return True


def insert_new_user(new_user: str, team: int) -> bool:
    with psycopg2.connect(**db_params) as con:  # type: ignore
        with con.cursor() as cur:
            query = """
                    INSERT INTO volunteers (name,team_id)
                    VALUES (%s, %s)
                    """
            cur.execute(query, (new_user, team))
            con.commit()
            return True


def validate_user(new_user: str | None) -> tuple[bool, str | None]:
    # returns message if new username is not valid
    if new_user is None or new_user.strip() == "":
        return False, "Please enter a valid name"

    new_user = new_user.strip()

    if len(new_user) < 3:
        return False, "Name must be at least 3 characters long"

    if not is_username_available(new_user):
        return False, "User already exists. Please choose different name"

    return True, None


def get_teams(cur) -> dict:
    query = """
            SELECT 
                t.id,
                t.team_name
            FROM teams t
            """
    cur.execute(query)
    res = cur.fetchall()
    if res:
        return {r[0]: r[1] for r in res}
    return {}


def register_callbacks(app):

    @app.callback(
        Output("new-user-modal", "is_open", allow_duplicate=True),
        Input("new-user-modal-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def new_user_callback2(n_clicks: int):
        if not n_clicks:
            return no_update
        return True

    @app.callback(Output("new-user-team-input", "options"), Input("url", "pathname"))
    def populate_teams_dropdown(url: str) -> dict:
        if not url == "/admin":
            return no_update
        with psycopg2.connect(**db_params) as con:  # type: ignore
            with con.cursor() as cur:
                return get_teams(cur)

    @app.callback(
        Output("user-store", "data", allow_duplicate=True),
        Output("new-user-error", "children", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Input("new-user-button", "n_clicks"),
        State("new-user-input", "value"),
        State("new-user-team-input", "value"),
    )
    def submit_new_user(n_clicks: int, new_user: str, team: str):
        if not n_clicks:
            return no_update

        success, msg = validate_user(new_user)
        if success:
            insert_new_user(new_user, team)
            return new_user, "", "/hours"
        else:
            return no_update, msg, no_update

    @app.callback(
        Output("export-modal", "is_open", allow_duplicate=True),
        Input("open-export-modal", "n_clicks"),
    )
    def open_export_modal(n_clicks: int | None) -> bool:
        if n_clicks is None:
            return no_update
        return True

    @app.callback(
        Output("export-dates", "max_date_allowed"),
        Output("export-dates", "start_date"),
        Input("export-modal", "is_open"),
    )
    def update_max_date(is_open):
        if is_open:
            start_date = date.today() - pd.tseries.offsets.MonthBegin(1)
            return date.today(), start_date
        return no_update

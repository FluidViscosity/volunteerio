from dash import Output, Input, no_update, State
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

            # add new user
            query = """
                    INSERT INTO volunteers (name)
                    VALUES (%s)
                    """
            cur.execute(query, (new_user,))
            con.commit()
    return True


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

    @app.callback(
        Output("user-store", "data", allow_duplicate=True),
        Output("new-user-error", "children", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Input("new-user-button", "n_clicks"),
        State("new-user-input", "value"),
    )
    def submit_new_user(n_clicks: int, new_user: str):
        if not n_clicks:
            return no_update
        if new_user is None or new_user.strip() == "":
            return (
                no_update,
                "Please enter a valid name.",
                no_update,
            )
        new_user = new_user.strip()
        if len(new_user) < 3:
            return (
                no_update,
                "Name must be at least 3 characters long.",
                no_update,
            )
        if is_username_available(new_user):
            return new_user, "", "/hours"
        else:
            return (
                no_update,
                "User already exists. Please choose a different name.",
                no_update,
            )

    @app.callback(
        Output("export-modal", "is_open", allow_duplicate=True),
        Input("open-export-modal", "n_clicks"),
    )
    def open_export_modal(n_clicks: int | None) -> bool:
        if n_clicks is None:
            return no_update
        return True

    @app.callback(
        Output("export-dates", "max_date_allowed"), Input("export-modal", "is_open")
    )
    def update_max_date(is_open):
        if is_open:
            return date.today()
        return no_update

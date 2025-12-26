from dash import Output, Input, no_update, State
import psycopg2

from volunteerio.db_config import db_params


def register_login_callbacks(app):
    @app.callback(
        Output("username-input", "options", allow_duplicate=True),
        Input("url", "pathname"),
    )
    def populate_users(path: str):
        if path is None or (path != "/login" and path != "/"):
            return no_update

        with psycopg2.connect(**db_params) as con:  # type: ignore
            with con.cursor() as cur:
                query = """
                        SELECT volunteers.name
                        FROM volunteers
                        WHERE volunteers.is_active=TRUE;
                        """
                cur.execute(query)
                res = cur.fetchall()
                res = [x[0] for x in res]
                if res is None:
                    raise Exception("Can't find users")
        return res

    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Output("user-store", "data", allow_duplicate=True),
        Input("login-button", "n_clicks"),
        State("username-input", "value"),
        prevent_initial_call=True,
    )
    def login_user(n_clicks, user):

        if not n_clicks:
            return no_update
        if user == None:
            return no_update

        else:
            return "/hours", user

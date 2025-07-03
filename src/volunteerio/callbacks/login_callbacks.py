from dash import Output, Input, no_update, State
import psycopg2

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
                if new_user == str(user[0]):
                    return False

            # add new user
            query = """
                    INSERT INTO volunteers (name,email)
                    VALUES (%s,'')
                    """
            cur.execute(query, (new_user,))
    return True


def register_login_callbacks(app):
    @app.callback(Output("username-input", "options"), Input("url", "pathname"))
    def populate_users(path: str):
        if path is None or (path != "/login" and path != "/"):
            return no_update

        with psycopg2.connect(**db_params) as con:  # type: ignore
            with con.cursor() as cur:
                query = """
                        SELECT volunteers.name
                        FROM volunteers;
                        """
                cur.execute(query)
                res = cur.fetchall()
                res = [x[0] for x in res]
                if res is None:
                    raise Exception("Can't find users")
                res.append("Add new...")
        return res

    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        Output("new-user-modal", "is_open", allow_duplicate=True),
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

        if user == "Add new...":
            return no_update, True, ""
        else:
            return "/hours", False, user

    @app.callback(
        Output("user-store", "data", allow_duplicate=True),
        Output("new-user-modal", "is_open", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
        Input("new-user-button", "n_clicks"),
        State("new-user-input", "value"),
        prevent_inital_call=True,
    )
    def new_user_callback(n_clicks: int, new_user):
        if n_clicks is None:
            return no_update
        if is_username_available(new_user):
            return new_user, False, "/hours"

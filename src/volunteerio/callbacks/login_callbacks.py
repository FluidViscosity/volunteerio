from dash import Output, Input, no_update, State


def is_username_available(user: str) -> bool:
    return True


def register_login_callbacks(app):
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

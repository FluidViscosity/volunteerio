from threading import Timer
import webbrowser
from volunteerio.main import app

from waitress import serve


def open_browser() -> None:
    webbrowser.open_new("http://localhost:8050")


if __name__ == "__main__":
    # Timer(1, open_browser).start()
    # app.run(debug=True, port=8050, use_reloader=False)
    serve(app.server, host="0.0.0.0", port=8050)

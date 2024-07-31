#!/usr/bin/env python3
""" Basic Flask app """
from typing import Dict, Union

from flask import Flask, g, render_template, request
from flask_babel import Babel


class Config(object):
    """Configuration class for Babel"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

users: Dict[int, Dict[str, Union[str, None]]] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict[str, Union[str, None]], None]:
    """Returns a user dictionary or None"""
    user_id = request.args.get("login_as")
    if user_id is not None:
        user_id = int(user_id)
        return users.get(user_id)
    return None


@app.before_request
def before_request() -> None:
    """Executes before all other functions"""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """Determine the best match with our supported languages"""
    # Locale from URL parameters
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale
    # Locale from user settings
    user = get_user()
    if user and user["locale"] in app.config["LANGUAGES"]:
        return user["locale"]
    # Locale from request header
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index() -> str:
    """Route for index page"""
    return render_template("6-index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")

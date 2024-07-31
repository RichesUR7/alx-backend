#!/usr/bin/env python3
""" Basic Flask app """
from flask import Flask, render_template
from flask_babel import Babel


class Config(object):
    """Configuration class for Babel"""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route("/")
def index() -> str:
    """Route for index page"""
    return render_template("1-index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000")

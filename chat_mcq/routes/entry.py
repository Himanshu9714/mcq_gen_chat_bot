from flask import Blueprint
from flask import render_template

entry_page = Blueprint(
    "entry_page",
    __name__,
)


@entry_page.route("/")
def index():
    """Entry point of the app."""

    return render_template("index.html")

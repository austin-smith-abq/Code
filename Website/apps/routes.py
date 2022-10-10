from flask import render_template, redirect
from flask import current_app as app

@app.route("/")
def dashboard():
    return render_template("dashboard.html", active="dashboard")

@app.route("/new_user")
def new_user():
    return render_template("new_user.html", active="new_user")
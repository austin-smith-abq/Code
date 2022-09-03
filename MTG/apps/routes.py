from flask import render_template, redirect, jsonify, request, url_for
from flask import current_app as app
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func

from .forms import (
    CardForm,
)
from .Card import db, Card, TCG

admin = Admin(app, template_mode='bootstrap4')


@app.route("/")
def dashboard():
    return render_template("dashboard.html", active="dashboard")


@app.route("/add_card", methods=["GET", "POST"])
def add_card():
    form = CardForm()
    if form.validate_on_submit():
        card_name = form.card_name.data
        print(card_name)
        return redirect("/add_card")

    return render_template(
        "manage_cards/add_card.html", active="add_card", form=form
    )

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    search = request.args.get("q")
    if len(search) > 4:
        query = (
            db.session.query(TCG.cleanname)
            .filter(func.upper(TCG.cleanname).like(f"%{str(search.upper())}%"))
            .order_by(TCG.cleanname.asc())
        )

        results = [field.cleanname for field in query.all()]
        return jsonify(matching_results=results)
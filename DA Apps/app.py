from flask import Flask, render_template, redirect
from Forms import DocumentForm, UserForm, UserSearchForm
from Models import User
from flask_bootstrap import Bootstrap
from database import get_email_autocomplete, search_user_database


app = Flask(__name__)
app.config["SECRET_KEY"] = "C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb"
Bootstrap(app)


@app.route("/")
def dashboard():
    return render_template("dashboard.html", active="dashboard")


@app.route("/create_document", methods=["GET", "POST"])
def create_document():
    form = DocumentForm()
    if form.validate_on_submit():
        case_number = form.case_number.data
        print(case_number)
        return redirect("/create_document")

    return render_template(
        "document_generation/create_document.html", active="create_document", form=form
    )


@app.route("/new_user", methods=["GET", "POST"])
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        user_type = form.user_type.data
        user_id = form.user_id.data
        division = form.division.data
        title = form.title.data
        supervisor = form.supervisor.data

        user = User(
            first_name,
            last_name,
            user_type,
            user_id,
            division,
            title,
            supervisor,
        )
        user.add()

        return redirect("/new_user")

    return render_template(
        "user_management/new_user.html", active="new_user", form=form
    )

@app.route("/modify_user", methods=["GET", "POST"])
def modify_user():
    emails = get_email_autocomplete()
    search_form = UserSearchForm()
    form = UserForm()
    if search_form.validate_on_submit():
        search_user_database(search_form.email.data)
    if form.validate_on_submit():
        print('success')
    return render_template(
        "user_management/modify_user.html", active="modify_user", search_form=search_form, form=form, emails=emails,
    )

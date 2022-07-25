from flask import Flask, render_template, redirect
from Forms import DocumentForm, UserForm, UserSearchForm, ContactForm, ContactSearchForm, GoogleSheetForm
from Models import User, Contact
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
@app.route("/new_contact", methods=["GET", "POST"])
def new_contact():
    form = ContactForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        agency = form.agency.data
        badge_id = form.badge_id.data
        title = form.title.data
        primary_phone = form.primary_phone.data
        cell_phone = form.cell_phone.data
        email = form.email.data

        contact = Contact(
            first_name,
            last_name,
            agency,
            badge_id,
            title,
            primary_phone,
            cell_phone,
            email,
        )
        contact.add()

        return redirect("/new_contact")

    return render_template(
        "contacts/new_contact.html", active="new_contact", form=form
    )

@app.route("/modify_contact", methods=["GET", "POST"])
def modify_contact():
    emails = get_email_autocomplete()
    search_form = ContactSearchForm()
    form = ContactForm()
    if search_form.validate_on_submit():
        form.first_name.data = 'Austin'
        #search_user_database(search_form.email.data)
    if form.validate_on_submit():
        print('success')
    return render_template(
        "contacts/modify_contact.html", active="modify_contact", search_form=search_form, form=form, emails=emails,
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
        form.first_name.data = 'Austin'
        #search_user_database(search_form.email.data)
    if form.validate_on_submit():
        print('success')
    return render_template(
        "user_management/modify_user.html", active="modify_user", search_form=search_form, form=form, emails=emails,
    )

@app.route("/quick_check", methods=["GET", "POST"])
def quick_check():
    form = GoogleSheetForm()
    if form.validate_on_submit():
        print('success')
    return render_template(
        "quality_control/quick_check.html", active="quick_check", form=form)

@app.route("/case_repair", methods=["GET", "POST"])
def case_repair():
    form = GoogleSheetForm()
    if form.validate_on_submit():
        print('success')
    return render_template(
        "quality_control/case_repair.html", active="case_repair", form=form)

@app.route("/warehouse_log", methods=["GET", "POST"])
def warehouse_log():
    form = GoogleSheetForm()
    if form.validate_on_submit():
        print('success')
    return render_template(
        "quality_control/warehouse_log.html", active="warehouse_log", form=form)
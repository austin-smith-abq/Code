from flask import render_template, redirect
from flask import current_app as app
from .forms import (
    DocumentForm,
    PleaForm,
    UserForm,
    UserSearchForm,
    ContactForm,
    ContactSearchForm,
    GoogleSheetForm,
)
from .Person import db, User, Contact

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
        "legal_tools/create_document.html", active="create_document", form=form
    )

@app.route("/plea_approval", methods=["GET", "POST"])
def plea_approval():
    form = PleaForm()
    if form.validate_on_submit():
        case_number = form.case_number.data
        print(case_number)
        return redirect("/plea_approval")

    return render_template(
        "legal_tools/plea_approval.html", active="plea_approval", form=form
    )


@app.route("/new_contact", methods=["GET", "POST"])
def new_contact():
    form = ContactForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        agency = form.agency.data
        badge_id = form.badge_id.data
        primary_phone = form.primary_phone.data
        cell_phone = form.cell_phone.data
        email = form.email.data

        new_contact = Contact(
            first_name=first_name,
            last_name=last_name,
            agency=agency,
            badge_id=badge_id,
            primary_phone=primary_phone,
            cell_phone=cell_phone,
            email=email,
            active=True,
        )
        db.session.add(new_contact)
        db.session.commit()

        return redirect("/new_contact")

    return render_template(
        "contacts/new_contact.html", active="new_contact", form=form
    )

@app.route("/modify_contact", methods=["GET", "POST"])
def modify_contact():
    emails = {'Test1': 'Test1'}
    search_form = ContactSearchForm()
    form = ContactForm()
    if search_form.validate_on_submit():
        form.first_name.data = "Austin"
        # search_user_database(search_form.email.data)
    if form.validate_on_submit():
        print("success")
    return render_template(
        "contacts/modify_contact.html",
        active="modify_contact",
        search_form=search_form,
        form=form,
        emails=emails,
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
        start_date = form.start_date.data

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            user_id=user_id,
            division=division,
            title=title,
            supervisor=supervisor,
            start_date=start_date,
        )
        db.session.add(new_user)
        db.session.commit()

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
        form.first_name.data = "Austin"
        # search_user_database(search_form.email.data)
    if form.validate_on_submit():
        print("success")
    return render_template(
        "user_management/modify_user.html",
        active="modify_user",
        search_form=search_form,
        form=form,
        emails=emails,
    )


@app.route("/quick_check", methods=["GET", "POST"])
def quick_check():
    form = GoogleSheetForm()
    if form.validate_on_submit():
        print("success")
    return render_template(
        "quality_control/quick_check.html", active="quick_check", form=form
    )


@app.route("/case_repair", methods=["GET", "POST"])
def case_repair():
    form = GoogleSheetForm()
    if form.validate_on_submit():
        print("success")
    return render_template(
        "quality_control/case_repair.html", active="case_repair", form=form
    )


@app.route("/warehouse_log", methods=["GET", "POST"])
def warehouse_log():
    form = GoogleSheetForm()
    if form.validate_on_submit():
        print("success")
    return render_template(
        "quality_control/warehouse_log.html", active="warehouse_log", form=form
    )

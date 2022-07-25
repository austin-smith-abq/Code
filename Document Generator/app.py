from flask import Flask, render_template, redirect
from Forms import DocumentForm, EmployeeForm, EmployeeSearchForm
from Models import Employee
from flask_bootstrap import Bootstrap
from database import get_email_autocomplete, search_employee_database


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


@app.route("/new_employee", methods=["GET", "POST"])
def new_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        employee_id = form.employee_id.data
        division = form.division.data
        title = form.title.data

        employee = Employee(
            first_name,
            last_name,
            employee_id,
            division,
            title,
        )
        employee.add()

        return redirect("/new_employee")

    return render_template(
        "employee_management/new_employee.html", active="new_employee", form=form
    )

@app.route("/search_employee", methods=["GET", "POST"])
def search_employee():
    emails = get_email_autocomplete()
    search_form = EmployeeSearchForm()
    form = EmployeeForm()
    if search_form.validate_on_submit():
        search_employee_database(search_form.email.data)
    if form.validate_on_submit():
        print('success')
    return render_template(
        "employee_management/search_employee.html", active="search_employee", search_form=search_form, form=form, emails=emails,
    )

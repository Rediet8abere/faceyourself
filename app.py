from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm
import os
from user import user


client = MongoClient()
db = client.faceyourself
employees = db.employees
comments = db.comments
companies = db.companies

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f324912c56dd495dc348bfd3cf23882dd80a483e190c5c78'

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    """Create a new account."""
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if employees.find_one({"username": form.username.data}):
                flash(f'That account already exists')
                return redirect(url_for('index'))
            else:
                current_user = employees.insert_one(user(form.username.data, form.password.data, form.email.data).json())
                return redirect(url_for('index'))
        else:
            flash(f'Incorrect crednetials')
            return render_template('register.html', form=form)

    if request.method == 'GET':
        return render_template('register.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Enables user to login"""
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if employees.find_one({"email": form.email.data}):
                if (form.email.data == employees.find_one({"email": form.email.data})["email"]) and (form.password.data == employees.find_one({"email": form.email.data})["password"]):
                    return redirect(url_for('add_company'))
            else:
                flash(f'Log in unsuccessful. Please Check password and email', 'danger')
    return render_template('login.html', form=form)

    if request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/add/company', methods = ['GET', 'POST'])
def add_company():
    """Add Company."""
    if request.method == 'POST':
        company = {
            'title': request.form.get('title'),
            'description': request.form.get('description')
            }
        companies.insert_one(company)
        return redirect(url_for('show_companies'))

    if request.method == 'GET':
        return render_template('company/add_company.html')

@app.route('/companies/show')
def show_companies():
    """Show all companies."""
    return render_template('company/show_companies.html', companies=companies.find())

# @app.route('/companies/<company_id>')
# def show_companies(company_id):
#     """Show all companies."""
#     company = companies.find_one({'_id': ObjectId(company_id)})
#     return render_template('company/show_companies.html', company=company)

@app.route('/comment', methods = ['GET', 'POST'])
def comment():
    """commentpage."""
    if request.method == 'POST':
        comment = {
            'title': request.form.get('title'),
            'content': request.form.get('content')
            }
        comments.insert_one(comment)
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('partials/comment_form.html')

@app.route('/showcomment')
def show_comment():
    """view all comment."""
    return render_template('partials/show_comments.html', comments = comments.find())

if __name__ == '__main__':
    app.run(debug=True)

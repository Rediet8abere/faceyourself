from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm
import os
from user import user


client = MongoClient()
db = client.faceyourself
users = db.users

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
            if users.find_one({"username": form.username.data}):
                flash(f'That account already exists')
                return redirect(url_for('index'))
            else:
                current_user = users.insert_one(user(form.username.data, form.password.data, form.email.data).json())
                return redirect(url_for('index'))
        else:
            flash(f'Incorrect crednetials')
            return render_template('register.html', form=form)

    if request.method == 'GET':
        return render_template('register.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Takes user to regestration page"""
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if users.find_one({"email": form.email.data}):
                if (form.email.data == users.find_one({"email": form.email.data})["email"]) and (form.password.data == users.find_one({"email": form.email.data})["password"]):
                    return redirect(url_for('movies_index'))
            else:
                flash(f'Log in unsuccessful. Please Check password and email', 'danger')
    return render_template('login.html', form=form)

    if request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/comment')
def comment():
    """commentpage."""
    # return "holla"
    return render_template('comment_form.html')

if __name__ == '__main__':
    app.run(debug=True)

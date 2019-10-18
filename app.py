from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm
import os
from user import user

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Playlister')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
employees = db.employees
companies = db.companies

app = Flask(__name__, static_url_path='',
            static_folder='templates/static')


app.config['SECRET_KEY'] = 'f324912c56dd495dc348bfd3cf23882dd80a483e190c5c78'

@app.route('/')
def index():
    """Return homepage."""
    return render_template('index.html')

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
                    return redirect(url_for('show_companies'))
            else:
                flash(f'Log in unsuccessful. Please Check password and email', 'danger')
    return render_template('login.html', form=form)

    if request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/companies/show')
def show_companies():
    """Show all companies."""
    return render_template('company/show_companies.html', companies=companies.find())

@app.route('/add/company', methods = ['GET', 'POST'])
def add_company():
    """Add Company."""
    if request.method == 'POST':
        company = {
            'name': request.form.get('name'),
            'description': request.form.get('description')
            }
        companies.insert_one(company)
        return redirect(url_for('show_companies'))

    if request.method == 'GET':
        return render_template('company/add_company.html')

@app.route('/comment/<company_id>', methods = ['GET', 'POST'])
def comment(company_id):
    """commentpage."""
    if request.method == 'POST':
        comment = { "comment": {
                    'id': request.form.get('id'),
                    'title': request.form.get('title'),
                    'content': request.form.get('content')
        }}
        companies.update_one(
        {'_id': ObjectId(company_id)},
        {'$push': comment})
        return redirect(url_for('show_add', company_id=company_id))

    if request.method == 'GET':
        return render_template('partials/comment_form.html', company_id=company_id)

@app.route('/show/add/<company_id>')
def show_add(company_id):
    """option to show or add comments."""
    company = companies.find_one({'_id': ObjectId(company_id)})
    return render_template('partials/show_add.html', company=company)

@app.route('/showcomment/<company_id>')
def show_comment(company_id):
    """view all comment."""
    company = companies.find_one({'_id': ObjectId(company_id)})
    return render_template('partials/show_comments.html', company=company)
# I have to get the companies id and the comments id
@app.route('/comment/<comment_id>/<company_id>/delete', methods = ['GET', 'POST'])
def comment_delete(comment_id, company_id):
    """Delete one comment."""
    print("asdasda")
    # return render_template('delete_edit.html', comment_id=comment_id, company_id=company_id)
    if request.method == 'GET':
        print("GET")
        return render_template('delete_edit.html', comment_id=comment_id, company_id=company_id)
    if request.method == 'POST':
        # print("In here")
        # return f'{comment_id}, {company_id}'

        # db.profiles.update( { _id: 1 }, { $pull: { votes: { $gte: 6 } } } )
        # { $pull: { <field1>: <value|condition>, <field2>: <value|condition>, ... } }
        print("Post")
        # companies.update_one(
        # {'_id': ObjectId(company_id)},
        # {'$pull': {"comment" : f"{comment_id}"}})

        #TODO: Find and store the entire array of comments for company database

        for index, comment in enumerate(comment_array):
            if comment._id == comment_id:
                del[index]


        # TODO: Update field to newly created array


        companies.update(
        {'_id': ObjectId(company_id)},
        {'$pull': {"comment" : {"_id":f"{comment_id}"}}})

        # { $pull: { <field1>: <value|condition>, <field2>: <value|condition>, ... } }

        # companies.update(
        #     { },
        #     { $pull: { comment: { $in: [ "apples", "oranges" ] }, vegetables: "carrots" } },
        #     { multi: true }
        # )

        # print("POST")
        # companies.find_one_and_update({"_id": ObjectId(company_id)},
        #                          {"$set": {"comment": []}})
        # companies.delete_one({'_id': ObjectId(company_id)})

        print("HERE2")
        return redirect(url_for('index'))
    # companies.delete_one({'_id': ObjectId(comment_id)})
    # return redirect(url_for('show_comment', company_id=company_id))




if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

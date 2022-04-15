from flask import (Flask, render_template, request, redirect)
from jinja2 import StrictUndefined
from model import connect_to_db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, validators
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
import crud
import os
import datetime
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
csrf = CSRFProtect(app)
app.jinja_env.undefined = StrictUndefined
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class UserForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired(), validators.Length(
        min=3, max=25)], render_kw={"placeholder": "Name"})
    email = StringField('Email', [validators.DataRequired(), validators.Length(
        min=3, max=25)], render_kw={"placeholder": "Email"})
    birthday = DateField('Birthday', [validators.DataRequired()])
    zip_code = StringField('Zip Code', [validators.DataRequired(), validators.Length(min=5, max=5), Regexp(
        regex='\d', message="You must only use numbers")], render_kw={"placeholder": "Zip Code"})
    save = SubmitField(label=('Save'))

    def validate_date(self, birthday):
        if self.birthday.data >= datetime.date.today():
            raise ValidationError(
                f"Your birthday cannot be today or in the future!")

    def validate_email(self, email):
        if "@" not in self.email.data:
            raise ValidationError(
                f"You must input a full email address")


@ app.route('/', methods=["GET", "POST"])
def homepage():
    user_form = UserForm()
    users = crud.get_users()

    if request.method == 'POST' and user_form.validate():
        name = request.form.get('name')
        email = request.form.get('email')
        birthday = request.form.get('birthday')
        zip_code = request.form.get('zip_code')

        user = crud.create_user(name, email, birthday, zip_code)
        print("*********************", "USER:", user, "********************")

        return redirect('/')

    return render_template('homepage.html', users=users, form=user_form)


@ app.route('/update/<user_id>', methods=["GET", "POST"])
def update_user(user_id):

    user = crud.get_user_by_id(user_id)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        birthday = request.form.get('birthday')
        zip_code = request.form.get('zip_code')

        new_user = crud.update_user(user_id, name, email, birthday, zip_code)
        print("****************", "USER UPDATED", new_user, "****************")

        return redirect('/')

    return render_template('update.html', user=user)


@ app.route('/delete/<user_id>', methods=["GET", "POST"])
def delete_user(user_id):

    crud.delete_user(user_id)
    print("****************", "USER DELETED", "****************")

    return redirect('/')


if __name__ == '__main__':
    from flask import Flask

    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

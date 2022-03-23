from flask import (Flask, render_template, request,
                   flash, session, jsonify, redirect)
from jinja2 import StrictUndefined
from model import connect_to_db
import crud

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


@app.route('/', methods=["GET", "POST"])
def homepage():

    users = crud.get_users()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        birthday = request.form.get('birthday')
        zip_code = request.form.get('zip_code')

        user = crud.create_user(name, email, birthday, zip_code)
        print("*********************", "USER:", user, "********************")

        return redirect('/')

    return render_template('homepage.html', users=users)


@app.route('/update/<user_id>', methods=["GET", "POST"])
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


@app.route('/delete/<user_id>', methods=["GET", "POST"])
def delete_user(user_id):

    crud.delete_user(user_id)
    print("****************", "USER DELETED", "****************")

    return redirect('/')


if __name__ == '__main__':
    from flask import Flask

    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

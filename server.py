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
    print(users)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        birthday = request.form.get('birthday')
        zip_code = request.form.get('zip_code')

        user = crud.create_user(name, email, birthday, zip_code)
        print("********************************", "USER:",
              user, "*******************************")

        return redirect('/')

    return render_template('homepage.html', users=users)


@app.route('/update_table')
def update_table():

    return redirect('/')


if __name__ == '__main__':
    from flask import Flask

    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)

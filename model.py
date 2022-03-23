from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    birthday = db.Column(db.Date, nullable=False,
                         default=datetime.date(1923, 10, 16))
    zip_code = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.name} email={self.email} birthday={self.birthday} zip_code={self.zip_code}'


def connect_to_db(flask_app, db_uri='postgresql:///people-flask', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == "__main__":
    from server import app

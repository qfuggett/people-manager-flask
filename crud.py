from model import db, User


def create_user(name, email, birthday, zip_code):

    user = User(name=name, email=email, birthday=birthday, zip_code=zip_code)

    db.session.add(user)
    db.session.commit()

    return user


def get_users():
    """Returns all users in database"""

    return User.query.all()


def get_user_by_id(user_id):
    """Returns a user by id"""

    return User.query.filter(User.user_id == user_id).first()


def update_user(user_id, name, email, birthday, zip_code):
    """Updates a user by id"""

    user = get_user_by_id(user_id)
    user.name = name
    user.email = email
    user.birthday = birthday
    user.zip_code = zip_code

    db.session.add(user)
    db.session.commit()

    return user


def delete_user(user_id):
    """Deletes a user by id"""

    User.query.filter(User.user_id == user_id).delete()

    return db.session.commit()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

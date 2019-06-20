from models import User, UserSchema, ContactDetail
from flask import make_response, abort
from config import db


def read_all():
    '''
    Retrieves a list of all users from the database.
    :return: list
    '''
    # get list of users
    users = User.query.order_by(User.username).all()

    # convert list to a string
    user_schema = UserSchema(many=True)
    data = user_schema.dump(users)

    return data


def get_by_id(user_id):
    '''
    Retrieves a user for given id if such one exists in the database.
    :param user_id: int
    :return: dict
    '''
    # retrieve an existing user
    user = (
        User.query.filter(User.user_id == user_id)
        .outerjoin(ContactDetail)
        .one_or_none()
    )

    if not user:
        abort(404, 'Failed to find user with id: {}'.format(user_id))

    # convert db object to a string
    user_schema = UserSchema()
    data = user_schema.dump(user)

    return data


def create(user):
    '''
    Creates a new user.
    :param user: str
    :return: dict, 201 - in case of success
    '''
    username = user.get('username')

    exisiting_user = (
        User.query.filter(User.username == username)
        .one_or_none()
    )

    if exisiting_user:
        abort(409, 'Found existing user with username: {}'.format(username))

    # create new user
    schema = UserSchema()
    new_user = schema.load(user, session=db.session)
    db.session.add(new_user)
    db.session.commit()

    data = schema.dump(new_user)
    return data, 201


def update(user_id, user):
    '''
    Updates user with given id.
    :param user_id: integer
    :param user: object
    :return: dict, 200 - in case of success
    '''
    update_user = User.query.filter(User.user_id == user_id).one_or_none()

    if not update_user:
        abort(404, 'Failed to find user with id: {}'.format(user_id))

    # retrieve user object from database
    schema = UserSchema()
    update = schema.load(user, session=db.session)

    # update user
    update.user_id = update_user.user_id
    db.session.merge(update)
    db.session.commit()

    data = schema.dump(update_user)
    return data, 200


def delete(user_id):
    '''
    Deletes a user with given id.
    :param user_id: int
    :return: str, 200 - in case of success
    '''
    user = User.query.filter(User.user_id == user_id).one_or_none()

    if not user:
        abort(404, 'Failed to find user with id: {}'.format(user_id))

    # remove user from the database
    db.session.delete(user)
    db.session.commit()

    return make_response(f'User {user_id} deleted', 200)
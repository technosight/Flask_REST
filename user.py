from models import User, UserSchema, Email
from flask import make_response, abort
from config import db


def read_all():

    users = User.query.order_by(User.username).all()
    user_schema = UserSchema(many=True)
    data = user_schema.dump(users)
    return data


def read_by_id(user_id):

    user = (
        User.query.filter(User.id == user_id)
        .outerjoin(Email)
        .one_or_none()
    )
    if user:
        user_schema = UserSchema()
        data = user_schema.dump(user)
        return data


def create(user):

    username = user.get('username')
    # first_name = user.get('first_name')
    # surname = user.get('surname')

    exisiting_user = (
        User.query.filter(User.username == username)
        .one_or_none()
    )

    if exisiting_user:
        abort(409, f'User with username {username} already exists')
    else:
        schema = UserSchema()
        new_user = schema.load(user, session=db.session)
        db.session.add(new_user)
        db.session.commit()

        data = schema.dump(new_user)
        return data, 201


def update(user_id, user):

    update_user = User.query.filter(User.id == user_id).one_or_none()

    if not update_user:
        abort(404, f'User not found for id: {user_id}')
    else:
        schema = UserSchema()
        update = schema.load(user, session=db.session)

        update.id = update_user.id
        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_user)
        return data, 200


def delete(user_id):

    user = User.query.filter(User.id == user_id).one_or_none()

    if not user:
        abort(404, f'User not found for id: {user_id}')
    else:
        db.session.delete(user)
        db.session.commit()

        return make_response(f'User {user_id} deleted', 200)
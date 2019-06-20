from models import ContactDetail, ContactDetailSchema, User
from flask import make_response, abort
from config import db


def get_by_id(user_id, contact_detail_id):
    '''
    Retrieves a contact detail by given user id and contact detail id.
    :param user_id: int
    :param contact_detail_id: int
    :return: dict
    '''
    # retrieves a record from the database
    contact_detail = (
        ContactDetail.query.join(User, User.user_id == ContactDetail.user_id)
        .filter(User.user_id == user_id)
        .filter(ContactDetail.contact_detail_id == contact_detail_id)
        .one_or_none()
    )

    # validate the record
    if not contact_detail:
        abort(404, 'Failed to find contact detail with id: {}'.format(contact_detail_id))

    # convert the record to dict
    contact_detail_schema = ContactDetailSchema()
    data = contact_detail_schema.dump(contact_detail)

    return data


def create(user_id, contact_detail):
    '''
    Create new contact detail for given user.
    :param user_id: id
    :param contact_detail: object
    :return: dict, 201 - in case of success
    '''
    # validate user
    user = User.query.filter(User.user_id == user_id).one_or_none()
    if not user:
        abort(404, 'Failed to find a user with id: {}'.format(user_id))

    # validate email
    existing_contact_detail = ContactDetail.query.filter(ContactDetail.email == contact_detail.get('email')).one_or_none()
    if existing_contact_detail:
        abort(404, 'Given email already exists: {}'.format(contact_detail.get('email')))

    # create new contact detail and attach it to the user
    contact_detail_schema = ContactDetailSchema()
    new_contact_detail = contact_detail_schema.load(contact_detail, session=db.session)
    user.contact_details.append(new_contact_detail)
    db.session.commit()

    result = contact_detail_schema.dump(new_contact_detail)

    return result, 201


def update(user_id, contact_detail_id, contact_detail):
    '''
    Update contact detail for given user id and given contact detail id.
    :param user_id: int
    :param contact_detail_id: int
    :param contact_detail: obj
    :return: dict, 200 - in case of success
    '''
    existing_contact_detail = (
        ContactDetail.query.filter(User.user_id == user_id)
        .filter(ContactDetail.contact_detail_id == contact_detail_id)
        .one_or_none()
    )

    if not existing_contact_detail:
        abort(404, 'Failed to find contact detail with id: {}'.format(contact_detail_id))

    # convert input data into db object
    schema = ContactDetailSchema()
    update = schema.load(contact_detail, session=db.session)

    # set corresponding ids
    update.user_id = existing_contact_detail.user_id
    update.contact_detail_id = existing_contact_detail.contact_detail_id

    # commit updated record to the database
    db.session.merge(update)
    db.session.commit()

    # return updatd contact_detail
    data = schema.dump(update)

    return data, 200


def delete(user_id, contact_detail_id):
    '''
    Deletes contact detail for given user id and contact detail id.
    :param user_id: int
    :param contact_detail_id: int
    :return: str, 200 - in case of success
    '''
    contact_detail = (
        ContactDetail.query.filter(User.user_id == user_id)
        .filter(ContactDetail.contact_detail_id == contact_detail_id)
        .one_or_none()
    )

    if not contact_detail:
        abort(404, 'Failed to find contact detail with id: {}'.format(contact_detail_id))

    db.session.delete(contact_detail)
    db.session.commit()

    return make_response(
        'ContactDetails with id: {} is deleted'.format(contact_detail_id),
        200
    )
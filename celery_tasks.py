from celery import Celery
import user as user_api
import contact_detail as contact_detail_api
from datetime import datetime, timedelta
import utils
import pytz

utc=pytz.UTC

# create Celery application
app = Celery('celery_tasks', broker='redis://localhost', backend='redis://localhost')

app.conf.beat_schedule = {
    'create-contact-every-15-seconds': {
        'task': 'celery_tasks.create_contact',
        'schedule': 15.0
    },
    'delete-contacts-older-than-60-seconds': {
        'task': 'celery_tasks.delete_contact',
        'schedule': 60.0
    }

}
# disable UTC to let Celery use local time
app.conf.enable_utc = False

@app.task
def create_contact():
    '''
    creates new contact
    :return:
    '''
    name = utils.get_random_name()
    surname = utils.get_random_surname()
    username = f'{name[:1]}{surname}'
    new_user = {
        'username': username,
        'first_name': name,
        'surname': surname
    }
    print(f'creating new user: {username}')
    user, status = user_api.create(new_user)
    assert(status == 201)

    email = f'{username}@{utils.generate_random_string(6)}.com'
    print(f'creating new email: {email}')
    contact_detail = {
        'email': email
    }
    result, status = contact_detail_api.create(user.get('user_id'), contact_detail)
    assert(status == 201)

@app.task
def delete_contact():
    '''
    removes Contacts older than 1 minute
    :return:
    '''
    users = user_api.read_all()
    # normalise datetime
    now = datetime.now() - timedelta(minutes=1)
    now = now.replace(tzinfo=utc)
    for user in users:
        created_on = datetime.strptime(user.get('contact_details')[0].get('created_on'), '%Y-%m-%dT%H:%M:%S.%f%z')
        # normalise datetime
        created_on = created_on.replace(tzinfo=utc)
        if created_on < now:
            try:
                print(f'deleting user: {user.get("name")} {user.get("surname")}')
                user_api.delete(user.get('user_id'))
            except Exception as e:
                assert('Working outside of application context' in str(e))

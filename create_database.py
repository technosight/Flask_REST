import os
from datetime import datetime
from config import db
from models import User, ContactDetail
from datetime import datetime, timedelta

created_on = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
# sample data
USERS = [
    {
        'username': 'pkerry',
        'first_name': 'Paul',
        'surname': 'Kerry',
        'contact_details': [
            ('pkerry@mail.com'),
            ('pkerry@yahoo.com'),
            ('pkerry@gmail.com'),
        ],
    },
    {
        'username': 'tdean',
        'first_name': 'Tom',
        'surname': 'Dean',
        'contact_details': [
            ('tdean@mail.com'),
            ('tdean@yahoo.com'),
            ('tdean@gmail.com'),
        ],
    },
    {
        'username': 'adavies',
        'first_name': 'Anna',
        'surname': 'Davies',
        'contact_details': [
            ('adavies@mail.com'),
            ('adavies@yahoo.com'),
            ('adavies@gmail.com'),
        ],
    },
]

# delete old database file
print('deleting existing database..')
if os.path.exists('users.db'):
    os.remove('users.db')

# create new database
db.create_all()

# insert sample records
print('inserting a list of new records...')
for user in USERS:
    db_user = User(
        username=user.get('username'),
        first_name=user.get('first_name'),
        surname=user.get('surname')
    )

    # add emails
    contact_details = user.get('contact_details')
    for contact_detail in contact_details:
        db_user.contact_details.append(
            ContactDetail(
                email=contact_detail,
            )
        )
    db.session.add(db_user)

db.session.commit()

print('database is ready')
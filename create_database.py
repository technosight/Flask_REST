import os
from datetime import datetime
from config import db
from models import User, ContactDetail


# sample data
USERS = [
    {
        'username': 'pkerry',
        'first_name': 'Paul',
        'surname': 'Kerry',
        'contact_details': [
            ('pkerry@mail.com', '2019-06-12 12:00:00'),
            ('pkerry@yahoo.com', '2019-06-12 12:01:01'),
            ('pkerry@gmail.com', '2019-06-12 12:02:02'),
        ],
    },
    {
        'username': 'tdean',
        'first_name': 'Tom',
        'surname': 'Dean',
        'contact_details': [
            ('tdean@mail.com', '2019-06-12 12:00:00'),
            ('tdean@yahoo.com', '2019-06-12 12:01:01'),
            ('tdean@gmail.com', '2019-06-12 12:02:02'),
        ],
    },
    {
        'username': 'adavies',
        'first_name': 'Anna',
        'surname': 'Davies',
        'contact_details': [
            ('adavies@mail.com', '2019-06-12 12:00:00'),
            ('adavies@yahoo.com', '2019-06-12 12:01:01'),
            ('adavies@gmail.com', '2019-06-12 12:02:02'),
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
        email, created_on = contact_detail
        db_user.contact_details.append(
            ContactDetail(
                email=email,
                created_on=datetime.strptime(created_on, '%Y-%m-%d %H:%M:%S'),
            )
        )
    db.session.add(db_user)

db.session.commit()

print('database is ready')
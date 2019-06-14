import os
from datetime import datetime
from config import db
from models import User, Email


# sample data
USERS = [
    {
        "username": "pkerry",
        "first_name": "Paul",
        "surname": "Kerry",
        "emails": [
            ("pkerry@mail.com", "2019-06-12 12:00:00"),
            ("pkerry@yahoo.com", "2019-06-12 12:01:01"),
            ("pkerry@gmail.com", "2019-06-12 12:02:02"),
        ],
    },
    {
        "username": "tdean",
        "first_name": "Tom",
        "surname": "Dean",
        "emails": [
            ("tdean@mail.com", "2019-06-12 12:00:00"),
            ("tdean@yahoo.com", "2019-06-12 12:01:01"),
            ("tdean@gmail.com", "2019-06-12 12:02:02"),
        ],
    },
    {
        "username": "adavies",
        "first_name": "Anna",
        "surname": "Davies",
        "emails": [
            ("adavies@mail.com", "2019-06-12 12:00:00"),
            ("adavies@yahoo.com", "2019-06-12 12:01:01"),
            ("adavies@gmail.com", "2019-06-12 12:02:02"),
        ],
    },
]

# delete old database file
print('deleting existing database..')
if os.path.exists("users.db"):
    os.remove("users.db")

# create new database
db.create_all()

# insert sample records
print('inserting a list of new records...')
for contact in USERS:
    c = User(
        username=contact.get("username"),
        first_name=contact.get("first_name"),
        surname=contact.get("surname")
    )

    # add emails
    for email in contact.get("emails"):
        address, created_on = email
        c.emails.append(
            Email(
                address=address,
                created_on=datetime.strptime(created_on, "%Y-%m-%d %H:%M:%S"),
            )
        )
    db.session.add(c)

db.session.commit()

print('database is ready')
# RESTful API with Flask, Connextion and Marshmallow

## Overview

This is a sample implementation of RESTful API with Python 3, Flask, Connexion and Marshmallow. Swagger page provides a list of implemented API calls with an ability to test them.

Data model consists of two entities: a User and a ContactDetail. User has one-to-many relationship with ContactDetails.

SQLite is used as a backend database, it is represented by a single file and does not require any specific configuration.


## How to run the app

* Recreate the database if required:

`python create_database.py`

* Start up Flask server:

`python app.py`

* Open your web browser and navigate to:

`http://0.0.0.0:5000/api/ui`

* Use this Swagger page to browser API methods and test them.



# Test assignment

## Overview

This test implements RESTful API with Pythonb 3, Flask, Connexion and Marshmallow. Swagger page provides a list of implemented API calls with an ability to test them.

Current version contains API methods for Contacts only. Emails and Celery task are to be implemented. 

## How to run the test

* Recreate the database if required:

`python create_database.py`

* Start up Flask server:

`python app.py`

* Open your web browser and navigate to:

`http://0.0.0.0:5000/api/ui`

* Use this Swagger page to browser API methods and test them.



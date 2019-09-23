# RESTful API with Flask, Connextion, Marshmallow and Celery

## Overview

This is an implementation of RESTful API with Python 3, Flask, Connexion and Marshmallow. Swagger page provides a list of implemented API calls with an ability to test them. Celery runs 2 async tasks.

Data model consists of two entities: a User and a ContactDetail. User has one-to-many relationship with ContactDetails.

SQLite is used as a backend database, it is represented by a single file and does not require any specific configuration.

## RESTful API

Connexion framework automagically handles HTTP requests based on OpenAPI Specification (formerly known as Swagger Spec). Connexion allowed to define an OpenAPI specification of this API in `api.yml` file and then map the endpoints to API Python functions.

Marshmallow is an ORM library that converts complex datatypes, such as objects, to and from native Python datatypes. Unlike Flask-RESTful, which uses dictionaries to define output schemas, marshmallow uses classes defined in `models.py`. In this case marshmallow helped to produce output data in JSON format. 


## How to run the app

* Recreate the database if required:
```
cd {work_folder}/IQVIA
python create_database.py
```
* Run unit tests:
```
cd {work_folder}/IQVIA
python -m unittest utests.test_api
```
* Start up Flask server:
```
cd {work_folder}/IQVIA
python app.py
```
* Open your web browser and navigate to:
```
http://0.0.0.0:5000/api/ui
```
* Use this Swagger page to browser API methods and test them.
* You can stop the Flask app as Celery calls API functions directly without creating HTTP requests.
* Start Redis:
```
docker run -d -p 6379:6379 redis
```
* Start scheduler for Celery tasks:
```
cd {work_folder}/IQVIA
celery -A celery_tasks beat --loglevel=info
``` 
* Open new terminal and start Celery worker:
```
cd {work_folder}/IQVIA
celery -A celery_tasks worker --loglevel=info
```
* Open `users.db` file with SQLite browser and observe tables `user` and `contact_detail` being updated every 15 seconds.



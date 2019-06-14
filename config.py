# import os
from pathlib import Path
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# base_dir = os.path.abspath(os.path.dirname(__file__))
base_dir = Path(__file__).resolve().parent
db_file = base_dir / 'users.db'

# initialise connexion app
connex_app = connexion.App(__name__, specification_dir=base_dir)

# get handle to Flask app
app = connex_app.app

# configure sqlite with SQLAlchemy
app.config["SQLALCHEMY_ECHO"] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "users.db")
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///{}'.format(db_file)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialise database
db = SQLAlchemy(app)

# initialize marshmallow
ma = Marshmallow(app)

import os

import flask
import flask_sqlalchemy

basedir = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'floorplan.db'
FLOORPLAN_IMG_DIR_NAME = 'floorplan'
DB_PATH = os.path.join(basedir, DB_NAME)
FLOORPLAN_IMG_DIR = os.path.join(basedir, FLOORPLAN_IMG_DIR_NAME)
SQLITE_URL = f'sqlite:///{DB_PATH}'

app = flask.Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_URL
db = flask_sqlalchemy.SQLAlchemy(app)

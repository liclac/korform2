#!/usr/bin/env python
import os
from flask import Flask, render_template, send_file
from flask.ext.security import Security, SQLAlchemyUserDatastore
from werkzeug.utils import secure_filename
from assets import assets
from db import *
from forms import *
from admin import admin

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('keys')

db.init_app(app); db.app = app
assets.init_app(app)
admin.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/')
def index():
	return render_template("index.html")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

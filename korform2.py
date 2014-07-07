#!/usr/bin/env python
from flask import Flask, redirect, url_for, render_template
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required, current_user
from db import *
from assets import assets
from admin import admin
from forms import *

app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('keys')

db.init_app(app); db.app = app

assets.init_app(app)
admin.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.context_processor
def context_processor():
	suffix_overrides = { 'message': 'info' }
	return {
		'alert_class_suffix_for_message_category':
			lambda cat: suffix_overrides[cat] if cat in suffix_overrides else cat
	}

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/korister/')
@login_required
def korists():
	korists = Korist.query.filter_by(account=current_user)
	return render_template("korists.html", korists=korists)

@app.route('/korister/add/', methods=['GET', 'POST'])
@login_required
def korist_add():
	korist = Korist(account=current_user)
	form = KoristForm(obj=korist)
	if form.validate_on_submit():
		form.populate_obj(korist)
		db.session.add(korist)
		db.session.commit()
		return redirect(url_for('korists'))
	return render_template("korist_form.html", form=form)

@app.route('/korister/<id>/')
@login_required
def korist(id):
	korist = Korist.query.get(id)
	return render_template("korist.html", korist=korist)

@app.route('/korister/<id>/edit/', methods=['GET', 'POST'])
@login_required
def korist_edit(id):
	korist = Korist.query.get(id)
	form = KoristForm(obj=korist)
	if form.validate_on_submit():
		form.populate_obj(korist)
		db.session.add(korist)
		db.session.commit()
		return redirect(url_for('korist', id=korist.id))
	return render_template("korist_form.html", form=form)

@app.route('/kontaktpersoner/')
@login_required
def my_guardians():
	return render_template("my_guardians.html")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

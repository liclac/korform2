#!/usr/bin/env python
import re
from flask import Flask, redirect, url_for, render_template
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required, current_user
from jinja2 import evalcontextfilter, Markup, escape
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



class MyUserDatastore(SQLAlchemyUserDatastore):
	def create_user(self, **kwargs):
		if not 'profile' in kwargs:
			kwargs['profile'] = Profile()
		return super(SQLAlchemyUserDatastore, self).create_user(**kwargs)

user_datastore = MyUserDatastore(db, User, Role)
security = Security(app, user_datastore)



_paragraph_re = re.compile(r'(?:\r\n|\r(?!\n)|\n){2,}')
@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
	result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n')) \
		for p in _paragraph_re.split(escape(value)))
	if eval_ctx.autoescape:
		result = Markup(result)
	return result



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
	korists = Korist.query.filter_by(profile=current_user.profile)
	return render_template("korists.html", korists=korists)

@app.route('/korister/add/', methods=['GET', 'POST'])
@login_required
def korist_add():
	korist = Korist(profile=current_user.profile)
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
	return render_template("korist_form.html", korist=korist, form=form)

@app.route('/kontaktpersoner/')
@login_required
def guardians():
	guardians = Guardian.query.filter_by(profile=current_user.profile)
	return render_template("guardians.html", guardians=guardians)

@app.route('/kontaktpersoner/add/', methods=['GET', 'POST'])
@login_required
def guardian_add():
	if current_user.profile.guardians.count() >= 2:
		return redirect(url_for('guardians'))
	
	guardian = Guardian(profile=current_user.profile)
	form = GuardianForm(obj=guardian)
	if form.validate_on_submit():
		form.populate_obj(guardian)
		db.session.add(guardian)
		db.session.commit()
		return redirect(url_for('guardians'))
	return render_template("guardian_form.html", form=form)

@app.route('/kontaktpersoner/<id>/')
@login_required
def guardian(id):
	guardian = Guardian.query.get(id)
	return render_template("guardian.html", guardian=guardian)

@app.route('/kontaktpersoner/<id>/edit/', methods=['GET', 'POST'])
@login_required
def guardian_edit(id):
	guardian = Guardian.query.get(id)
	form = GuardianForm(obj=guardian)
	if form.validate_on_submit():
		form.populate_obj(guardian)
		db.session.add(guardian)
		db.session.commit()
		return redirect(url_for('guardian', id=guardian.id))
	return render_template("guardian_form.html", guardian=guardian, form=form)

@app.route('/kontaktpersoner/<id>/delete/', methods=['GET', 'POST'])
@login_required
def guardian_delete(id):
	guardian = Guardian.query.get(id)
	form = DeleteForm()
	if form.validate_on_submit():
		db.session.delete(guardian)
		db.session.commit()
		return redirect(url_for('guardians'))
	return render_template("guardian_delete.html", guardian=guardian, form=form)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

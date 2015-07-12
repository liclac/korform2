#!/usr/bin/env python
import re
import operator
from flask import Flask, current_app, abort, redirect, url_for, render_template
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required, current_user
from flask.ext.security.utils import encrypt_password
from flask.ext.mail import Mail
from flask.ext.migrate import Migrate
from jinja2 import evalcontextfilter, Markup, escape
from db import *
from assets import assets
from admin import admin
from forms import *

app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('keys')

mail = Mail(app)

db.init_app(app)
assets.init_app(app)
admin.init_app(app)

migrate = Migrate(app, db)



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

@app.template_filter()
def sort_multi(L,*operators):
	return sorted(L, key=operator.attrgetter(*operators))



@app.context_processor
def template_function_cproc():
	suffix_overrides = { 'message': 'info' }
	return {
		'alert_class_suffix_for_message_category':
			lambda cat: suffix_overrides[cat] if cat in suffix_overrides else cat
	}

@app.context_processor
def global_data_cproc():
	return {
		'all_groups': Group.query.all()
	}



@app.route('/')
def index():
	return render_template("index.html")

@app.route('/matrikel/')
@login_required
def matrikel():
	return render_template('matrikel.html')

@app.route('/matrikel/<group>/')
@login_required
def matrikel_group(group):
	group = Group.query.filter_by(slug=group).first()
	return render_template('matrikel_group.html', group=group)

@app.route('/korister/')
@login_required
def korists():
	korists = Korist.query.filter_by(profile=current_user.profile)
	return render_template("korists.html", korists=korists)

@app.route('/korister/add/')
@login_required
def korist_add():
	return render_template("korist_choose_group.html")

@app.route('/korister/add/<group>/', methods=['GET', 'POST'])
@login_required
def korist_add2(group):
	group = Group.query.filter_by(slug=group).first_or_404()
	korist = Korist(profile=current_user.profile, group=group, active=True)
	korist.osas = [ OSA(korist=korist, event=event) for event in korist.group.events ]
	form = KoristFormWithOSAs(obj=korist)
	if form.validate_on_submit():
		form.populate_obj(korist)
		korist.active = bool(form.active.data)
		db.session.add(korist)
		db.session.commit()
		return redirect(url_for('korists'))
	return render_template("korist_form.html", korist=korist, form=form)

@app.route('/korister/<id>/')
@login_required
def korist(id):
	korist = Korist.query.get_or_404(id)
	if korist.osas.count() == 0:
		return redirect(url_for('korist_osas', id=korist.id))
	return render_template("korist.html", korist=korist)

@app.route('/korister/<id>/edit/', methods=['GET', 'POST'])
@login_required
def korist_edit(id):
	korist = Korist.query.get_or_404(id)
	if korist.profile != current_user.profile and not current_user.has_role('Admin'):
		abort(403)
	if korist.osas.count() == 0:
		return redirect(url_for('korist_osas', id=korist.id))
	
	form = KoristForm(obj=korist)
	if form.validate_on_submit():
		form.populate_obj(korist)
		db.session.add(korist)
		db.session.commit()
		return redirect(url_for('korist', id=korist.id))
	return render_template("korist_form.html", korist=korist, form=form)

@app.route('/korister/<id>/osas/', methods=['GET', 'POST'])
@login_required
def korist_osas(id):
	korist = Korist.query.get_or_404(id)
	if korist.profile != current_user.profile and not current_user.has_role('Admin'):
		abort(403)
	if korist.osas.count() > 0:
		return redirect(url_for('korist_edit', id=korist.id))
	
	# form = OSASForm(obj=korist)
	form = KoristFormWithOSAs(obj=korist)
	if form.validate_on_submit():
		events = korist.group.events.all()
		for i in xrange(len(events)):
			osa_form = form.osas[i]
			osa = OSA(korist=korist, event=events[i], comment=osa_form.comment.data, osa=osa_form.osa.data)
			db.session.add(osa)
		
		# korist.active = bool(form.active.data)
		korist.populate_obj(korist)
		db.session.add(korist)
		
		db.session.commit()
		return redirect(url_for('korist', id=korist.id))
	else:
		for event in korist.group.events:
			form.osas.append_entry(OSA(korist=korist, event=event))
	# return render_template("korist_osas.html", korist=korist, form=form)
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
	return render_template("guardian_form.html", form=form, creating=True)

@app.route('/kontaktpersoner/<id>/')
@login_required
def guardian(id):
	guardian = Guardian.query.get_or_404(id)
	return render_template("guardian.html", guardian=guardian)

@app.route('/kontaktpersoner/<id>/edit/', methods=['GET', 'POST'])
@login_required
def guardian_edit(id):
	guardian = Guardian.query.get_or_404(id)
	if guardian.profile != current_user.profile:
		abort(403)
	
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
	guardian = Guardian.query.get_or_404(id)
	if guardian.profile != current_user.profile:
		abort(403)
	
	form = DeleteForm()
	if form.validate_on_submit():
		db.session.delete(guardian)
		db.session.commit()
		return redirect(url_for('guardians'))
	return render_template("guardian_delete.html", guardian=guardian, form=form)

@app.route('/settings/')
@login_required
def settings():
	return render_template("settings.html")

@app.route('/settings/password/', methods=['GET', 'POST'])
@login_required
def settings_password():
	form = PasswordForm()
	if form.validate_on_submit():
		current_user.password = encrypt_password(form.new_password.data)
		db.session.add(current_user)
		db.session.commit()
		return redirect(url_for('settings'))
	return render_template("settings_password.html", form=form)

'''
@app.route('/settings/sharing/', methods=['GET', 'POST'])
@login_required
def settings_shared():
	form=SharingInviteForm()
	if form.validate_on_submit():
		pass
	return render_template("settings_sharing.html", form=form)
'''

@app.errorhandler(404)
def error_404(e):
	return render_template("errors/404.html")

@app.errorhandler(403)
def error_403(e):
	if not current_user.is_authenticated():
		return current_app.login_manager.unauthorized()
	
	return render_template("errors/403.html")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')

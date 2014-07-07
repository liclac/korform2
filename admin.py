from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from wtforms import fields
from db import *

admin = Admin()

class RoleModelView(ModelView):
	form_overrides = { 'description': fields.TextAreaField }

class UserModelView(ModelView):
	column_exclude_list = ['password']
	form_excluded_columns = ['password']

class ProfileModelView(ModelView):
	column_list = ['users']

class KoristModelView(ModelView):
	column_list = ['group', 'first_name', 'last_name', 'phone', 'mobile', 'email']
	form_excluded_columns = ['osas']
	form_overrides = {
		'address_l1': fields.TextField,
		'address_l2': fields.TextField,
		'region': fields.TextField
	}

class GuardianModelView(ModelView):
	column_exclude_list = ['profile', 'comment']

class GroupModelView(ModelView):
	form_excluded_columns = ['members']

class EventModelView(ModelView):
	column_list = ['groups', 'title', 'dateline']
	form_excluded_columns = ['osas']

class OSAModelView(ModelView):
	column_labels = { 'osa': 'OSA' }
	column_choices = { 'osa': [(0, "Nej"), (1, "Ja"), (2, "Kanske")] }
	form_overrides = { 'osa': fields.SelectField }
	form_args = {
		'osa': {
			'choices': column_choices['osa'],
			'coerce': int
		}
	}

admin.add_view(RoleModelView(Role, db.session, endpoint='role'))
admin.add_view(UserModelView(User, db.session, endpoint='user'))
admin.add_view(ProfileModelView(Profile, db.session, endpoint='profile'))
admin.add_view(GuardianModelView(Guardian, db.session, endpoint='guardian'))
admin.add_view(KoristModelView(Korist, db.session, endpoint='korist'))
admin.add_view(GroupModelView(Group, db.session, endpoint='group'))
admin.add_view(EventModelView(Event, db.session, endpoint='event'))
admin.add_view(OSAModelView(OSA, db.session, name='OSA', endpoint='osa'))

from flask.ext.admin import Admin, AdminIndexView, BaseView
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.security import current_user
from wtforms import fields
from db import *

class AdminAuthMixin(object):
	def is_accessible(self):
		return current_user.has_role('Admin')

class MyAdminIndexView(AdminAuthMixin, AdminIndexView):
	pass

class MyBaseView(AdminAuthMixin, BaseView):
	pass

class MyModelView(AdminAuthMixin, ModelView):
	pass



class RoleModelView(MyModelView):
	form_overrides = { 'description': fields.TextAreaField }

class UserModelView(MyModelView):
	column_exclude_list = ['password']
	form_excluded_columns = ['password']

class ProfileModelView(MyModelView):
	column_list = ['users']

class KoristModelView(MyModelView):
	column_searchable_list = ['first_name', 'last_name']
	column_list = ['group', 'first_name', 'last_name', 'phone', 'mobile', 'email']
	form_excluded_columns = ['osas']
	form_overrides = {
		'address_l1': fields.TextField,
		'address_l2': fields.TextField,
		'region': fields.TextField
	}

class GuardianModelView(MyModelView):
	column_searchable_list = ['first_name', 'last_name']
	column_exclude_list = ['profile', 'comment']

class GroupModelView(MyModelView):
	form_excluded_columns = ['members']

class EventModelView(MyModelView):
	edit_template = 'admin/event_edit.html'
	column_list = ['groups', 'title', 'dateline', 'no_answer']
	form_excluded_columns = ['osas']

class OSAModelView(MyModelView):
	column_labels = { 'osa': 'OSA' }
	column_choices = { 'osa': [(1, "Ja"), (2, "Nej"), (3, "Kanske")] }
	form_overrides = { 'osa': fields.SelectField }
	form_args = {
		'osa': {
			'choices': column_choices['osa'],
			'coerce': int
		}
	}



admin = Admin(index_view=MyAdminIndexView())
admin.add_view(RoleModelView(Role, db.session, endpoint='role'))
admin.add_view(UserModelView(User, db.session, endpoint='user'))
admin.add_view(ProfileModelView(Profile, db.session, endpoint='profile'))
admin.add_view(GuardianModelView(Guardian, db.session, endpoint='guardian'))
admin.add_view(KoristModelView(Korist, db.session, endpoint='korist'))
admin.add_view(GroupModelView(Group, db.session, endpoint='group'))
admin.add_view(EventModelView(Event, db.session, endpoint='event'))
admin.add_view(OSAModelView(OSA, db.session, name='OSA', endpoint='osa'))


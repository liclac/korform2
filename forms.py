# coding=utf-8
from flask.ext.wtf import Form
from flask.ext.security import current_user
from flask.ext.security.utils import verify_password
from wtforms_alchemy import model_form_factory, ModelFieldList
from wtforms import fields, validators, widgets, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from db import *

BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
	@classmethod
	def get_session(self):
		return db.session

class PasswordForm(Form):
	old_password = fields.PasswordField(validators=[validators.required()])
	new_password = fields.PasswordField(validators=[validators.required()])
	new_password_again = fields.PasswordField(validators=[validators.required(),
		validators.EqualTo('new_password', "The passwords don't match")])
	
	def validate_old_password(form, field):
		if not verify_password(field.data, current_user.password):
			raise ValidationError('Incorrect password')

'''
class SharingInviteForm(Form):
	email = fields.TextField(validators=[validators.required()])
'''

class OSAForm(Form):
	osa = fields.RadioField(choices=[(1, u'Ja, jag räknar med att kunna vara med.'), (2, u'Nej, jag vet redan nu att jag inte kan vara med.'), (3, u'Jag kan inte lämna besked just nu.')], validators=[validators.required()], coerce=int)
	comment = fields.TextField()

class KoristForm(ModelForm):
	class Meta:
		model = Korist
		exclude = ['active']
	
	birthday = fields.DateField(validators=[validators.required()], widget=widgets.TextInput())

class KoristFormWithOSAs(KoristForm):
	class Meta:
		exclude = []
	
	active = fields.RadioField(choices=[(1, u'Ja, jag är med i Domkyrkans Goss- och Flickkörer/Ungdomskören höstterminen 2015'), (0, u'Nej, jag är inte med i höst, jag lämnar min plats till någon annan')], validators=[validators.InputRequired()], coerce=int, default=1)
	osas = fields.FieldList(fields.FormField(OSAForm))

class OSASForm(Form):
	active = fields.RadioField(choices=[(1, u'Ja, jag ska fortsätta i Domkyrkans Goss- och Flickkörer/Ungdomskören under vårterminen 2015'), (0, u'Nej, jag ska sluta i kören')], validators=[validators.InputRequired()], coerce=int, default=1)
	osas = fields.FieldList(fields.FormField(OSAForm))

class GuardianForm(ModelForm):
	class Meta:
		model = Guardian

class DeleteForm(Form):
	confirmation = fields.BooleanField(validators=[validators.required()])

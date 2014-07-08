from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory, ModelFieldList
from wtforms import fields, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from db import *

BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
	@classmethod
	def get_session(self):
		return db.session

class OSAForm(Form):
	osa = fields.RadioField(choices=[(1, 'Ja'), (2, 'Nej'), (3, 'Kanske')], validators=[validators.required()], coerce=int)

class KoristForm(ModelForm):
	class Meta:
		model = Korist
		exclude = ['active']
	
class KoristFormWithOSAs(KoristForm):
	osas = fields.FieldList(fields.FormField(OSAForm))

class GuardianForm(ModelForm):
	class Meta:
		model = Guardian

class DeleteForm(Form):
	confirmation = fields.BooleanField(validators=[validators.required()])

from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory
from db import *

BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
	@classmethod
	def get_session(self):
		return db.session

class KoristForm(ModelForm):
	class Meta:
		model = Korist
		exclude = ['active']

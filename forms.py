from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from db import *

GroupForm = model_form(Group, Form)
KoristForm = model_form(Korist, Form)
EventForm = model_form(Event, Form)
OSAForm = model_form(OSA, Form)

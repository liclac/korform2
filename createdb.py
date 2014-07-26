#!/usr/bin/env python
# coding=utf-8
import datetime
from flask.ext.security.utils import encrypt_password
from korform2 import *

with app.test_request_context():
	# Create database tables
	db.create_all()

	# Create default roles
	admin_role = user_datastore.create_role(name="Admin", description="Allowed to perform administrative tasks")

	# Create a default admin account
	admin_user = user_datastore.create_user(email='admin@localhost', password=encrypt_password('password'), active=True, confirmed_at=datetime.datetime.utcnow())
	user_datastore.add_role_to_user(admin_user, admin_role)
	
	# Create default groups
	groupdata = [
		(u'f0',  u'F asp', u'fasp',	u'Flickkörens aspiranter'),
		(u'f1',	 u'YF',   u'yf',	u'Yngre Flickkören'),
		(u'f2',	 u'ÄF',   u'af',	u'Äldre Flickkören'),
		(u'g0',	 u'G asp', u'gasp',	u'Gosskörens aspiranter'),
		(u'g1',	 u'GK',	  u'gk',	u'Gosskören'),
		(u'g1n', u'NI',	  u'ni',	u'Nissarna'),
		(u'zgu', u'GU',	  u'gu',	u'Gustavi Ungdomskör')
	]
	for data in groupdata:
		group = Group(sortcode=data[0], code=data[1], slug=data[2], name=data[3])
		db.session.add(group)
		db.session.commit()

	# Save changes
	db.session.commit()

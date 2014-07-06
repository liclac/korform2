from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin

db = SQLAlchemy()



role__user = db.Table('role__user',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean)
	confirmed_at = db.Column(db.DateTime)
	
	roles = db.relationship('Role', secondary=role__user, backref=db.backref('users', lazy='dynamic'))



event__group = db.Table('event__group',
	db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
	db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	can_apply_to = db.Column(db.Boolean)
	
	sortcode = db.Column(db.String(10), unique=True)
	code = db.Column(db.String(10), unique=True)
	name = db.Column(db.String(100), unique=True)
	
	members = db.relationship('Korist', backref='group', lazy='dynamic')
	
	def __str__(self):
		return self.code

class Korist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
	
	cont = db.Column(db.Boolean)
	
	first_name = db.Column(db.Text)
	last_name = db.Column(db.Text)
	parent_first_name = db.Column(db.Text)
	parent_last_name = db.Column(db.Text)
	
	address_l1 = db.Column(db.Text)
	address_l2 = db.Column(db.Text)
	post_code = db.Column(db.String(5))
	region = db.Column(db.Text)
	
	phone = db.Column(db.String(15))
	mobile = db.Column(db.String(15))
	email = db.Column(db.Text)
	
	guardian1 = db.Column(db.Text)
	guardian1_phone = db.Column(db.Text)
	guardian1_email = db.Column(db.Text)
	guardian2 = db.Column(db.Text)
	guardian2_phone = db.Column(db.Text)
	guardian2_email = db.Column(db.Text)
	
	birth_year = db.Column(db.Integer)
	birth_month = db.Column(db.Integer)
	birth_day = db.Column(db.Integer)
	
	allergies = db.Column(db.Text)
	other_info = db.Column(db.Text)
	
	osas = db.relationship('OSA', backref='korist', lazy='dynamic')
	
	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	title = db.Column(db.Text)
	dateline = db.Column(db.Text)
	description = db.Column(db.Text)
	
	groups = db.relationship('Group', secondary=event__group, backref=db.backref('events', lazy='dynamic'))
	osas = db.relationship('OSA', backref='event', lazy='dynamic')
	
	def __str__(self):
		return "%s (%s)" % (self.title, self.dateline)

class OSA(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	osa = db.Column(db.Integer)
	event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
	korist_id = db.Column(db.Integer, db.ForeignKey('korist.id'))

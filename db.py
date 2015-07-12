import re
import datetime
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
	
	def __str__(self):
		return self.name

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	
	profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
	
	email = db.Column(db.String(255), unique=True)
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean)
	confirmed_at = db.Column(db.DateTime)
	
	roles = db.relationship('Role', secondary=role__user, backref=db.backref('users', lazy='dynamic'))
	
	def __str__(self):
		return self.email

class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	users = db.relationship('User', backref='profile', lazy='joined')
	children = db.relationship('Korist', backref='profile', lazy='dynamic')
	guardians = db.relationship('Guardian', backref='profile', lazy='dynamic')
	
	def __str__(self):
		return 'Profile for %s' % (", ".join(u.email for u in self.users))
	



event__group = db.Table('event__group',
	db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
	db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)

korist__guardian = db.Table('korist__guardian',
	db.Column('korist_id', db.Integer, db.ForeignKey('korist.id')),
	db.Column('guardian_id', db.Integer, db.ForeignKey('guardian.id')),
)

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	sortcode = db.Column(db.String(10), unique=True, nullable=False)
	slug = db.Column(db.String(10), unique=True, nullable=False)
	code = db.Column(db.String(10), unique=True, nullable=False)
	name = db.Column(db.String(100), unique=True, nullable=False)
	
	# Make it default to sorting by sortcode, rather than the pk (id)
	__mapper_args__ = { 'order_by': sortcode }
	
	def __str__(self):
		return "%s (%s)" % (self.name, self.code)

class Guardian(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
	
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	phone = db.Column(db.String(15))
	phone2 = db.Column(db.String(15))
	email = db.Column(db.String(255))
	
	comment = db.Column(db.Text)
	private = db.Column(db.Boolean, nullable=False, default=False)
	
	__mapper_args__ = { 'order_by': [last_name, first_name] }
	
	def initials(self):
		r = re.compile(r' |-')
		fp = [p[0] for p in r.split(self.first_name) if p]
		lp = [p[0] for p in r.split(self.last_name) if p]
		return u''.join(fp) + u'.' + u''.join(lp) + u'.'
	
	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

class Korist(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
	
	active = db.Column(db.Boolean, default=True)
	group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
	group = db.relationship('Group', backref='members')
	
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	
	address1 = db.Column(db.Text, nullable=False)
	address2 = db.Column(db.Text)
	
	phone = db.Column(db.String(15), nullable=False)
	mobile = db.Column(db.String(15))
	email = db.Column(db.String(255))
	
	birthday = db.Column(db.Date, nullable=False)
	
	allergies = db.Column(db.Text)
	other_info = db.Column(db.Text)
	
	guardians = db.relationship('Guardian', secondary=korist__guardian, backref=db.backref('children', lazy='dynamic'))
	
	__mapper_args__ = { 'order_by': [last_name, first_name] }
	
	def public_guardians_with(self, attr):
		return [g for g in self.profile.guardians if not g.private and getattr(g, attr)]
	
	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	title = db.Column(db.Text, nullable=False)
	sort_date = db.Column(db.Date, nullable=False)
	dateline = db.Column(db.Text)
	description = db.Column(db.Text)
	no_answer = db.Column(db.Boolean)
	
	groups = db.relationship('Group', secondary=event__group, backref=db.backref('events', lazy='dynamic'))
	
	# Sort by the Sort Date, not the pk (id)
	__mapper_args__ = { 'order_by': (sort_date, id) }
	
	def __str__(self):
		return "%s (%s)" % (self.title, self.dateline)

class OSA(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	
	osa = db.Column(db.Integer, nullable=False)
	comment = db.Column(db.Text)
	
	event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
	event = db.relationship('Event', backref=db.backref('osas', cascade="delete"))
	korist_id = db.Column(db.Integer, db.ForeignKey('korist.id'))
	korist = db.relationship('Korist', backref=db.backref('osas', lazy='dynamic', cascade="delete"))
	
	# UI
	osa_strs = ['NULL', 'Ja', 'Nej', 'Kanske']
	osa_str = lambda self: self.osa_strs[self.osa]

	osa_unicodes = ['NULL', u'\u2713', u'x', u'?']
	osa_unicode = lambda self: self.osa_unicodes[self.osa]
	
	osa_class_suffixes = ['unknown', 'success', 'danger', 'warning']
	osa_class_suffix = lambda self: self.osa_class_suffixes[self.osa]

	osa_class_suffixes_bs2 = ['unknown', 'success', 'error', 'warning']
	osa_class_suffix_bs2 = lambda self: self.osa_class_suffixes_bs2[self.osa]
	
	def __str__(self):
		return "%s (%s)" % (self.event.title, self.osa_str())


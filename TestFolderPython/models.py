#Trent Lessig --> models.py --> set up entries into databases --> model part of mvc

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#following format of minitwit example given in class
#make username unique so we cannot have different people with same usernames
class USER(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), unique=True, nullable=False) 
	password_hash = db.Column(db.String(64), nullable=False)
	user_type = db.Column(db.String(64), nullable=False)
	
	eventCreated = db.relationship('SCHEDULING', backref='user')
	
#	staffList = db.relationship('SCHEDULING', secondary='event_staff', backref=db.backref('staff', lazy='dynamic'))
		
	def __init__(self, username, password_hash, user_type):    #constructor to create new user
		self.username = username
		self.password_hash = password_hash
		self.user_type = user_type
		
	def __repr__(self):
		return '<User {}>'.format(self.username) #string representation of user

#tried to do the many to many relationship but was confusing myself more than expected
#event_staff = db.Table('event_staff',
#	db.Column('event_id', db.Integer, db.ForeignKey('SCHEDULING.event_id')),
#	db.Column('staff_id', db.Integer, db.ForeignKey('USER.user_id')))


class SCHEDULING(db.Model):
	name = db.Column(db.String(24), nullable=False)
	date = db.Column(db.String(24), nullable=False)
	customer_id = db.Column(db.Integer, db.ForeignKey('USER.user_id'), nullable=False)
	event_id = db.Column(db.Integer, primary_key=True)
	staff1 = db.Column(db.String(24), default='-')
	staff2 = db.Column(db.String(24), default='-')
	staff3 = db.Column(db.String(24), default='-')
	
	def __repr__(self):
		return '<Scheduled Event {}'.format(self.date)

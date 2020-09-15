#Trent Lessig -- Catering.py --> create functionality --> controller aspect of mvc

import time
import os
from hashlib import md5
from datetime import datetime
from sqlalchemy import or_
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

from models import db, USER, SCHEDULING

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'catering.db')
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'development key'

app.config.from_object(__name__)
app.config.from_envvar('CATERING_SETTINGS', silent=True)

db.init_app(app)

ownerUsername = 'owner' #hard code owners username and password for easier testing
ownerPassword = 'pass'
owner = 'owner'  #make variables to hold a user type to allow for easier coding (to me anyway)
staff = 'staff'
customer = 'customer'


@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	db.create_all()
	db.session.add(USER(username=ownerUsername, password_hash=ownerPassword, user_type=owner))
	db.session.commit()
	#print(USER.query.all())
	print('Initialized the database.')

def get_user_id(username):
	"""Convenience method to look up the id for a username."""
	rv = USER.query.filter_by(username=username).first()
	return rv.user_id if rv else None
	
#grab all events to show owner and staff to sign up for
def all_events():
	rv = SCHEDULING.query.order_by(SCHEDULING.date).all()
	return rv if rv else []
	
#show customer events they have created
def customer_events():
	rv = g.user.eventCreated
	return rv if rv else []

#show staff events they have signed up for	
def staff_events(user_id):
	rv = SCHEDULING.query.filter(or_(SCHEDULING.staff1==user_id, SCHEDULING.staff2==user_id, SCHEDULING.staff3==user_id))
	return rv if rv else []
	
def check_date(schedule):
	rv = SCHEDULING.query.filter_by(date=schedule).first()
	return rv if rv else None

def format_datetime(timestamp):
	"""Format a timestamp for display."""
	return datetime.utcfromtimestamp(timestamp).strftime('%m-%d-%Y @ %H:%M')

@app.before_request
def before_request():
	g.user = None
	#print("ARE WE HERE")
	#print(session)
	if 'user_id' in session:
		#print("USER SHOULD BE IN SESH")
		g.user = USER.query.filter_by(user_id=session['user_id']).first()


#---------------------------SHOW ALL EVENTS TO GUESTS WHO ARENT SIGNED IN-------#
@app.route('/') #show all the events that are scheduled on the non logged in page
def home():	
	schedule = all_events()
	return render_template('account.html', schedule=schedule, availability=None)


#----------------------------------LOGIN A USER--------------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""
	if g.user:
		#print("why are we here")
		return redirect(url_for('show_account'))
	error = None
	if request.method == 'POST':

		user = USER.query.filter_by(username=request.form['username']).first()
		if user is None:
			error = 'Invalid username'
		elif user.password_hash != request.form['password']: #check that passwords match
			error = 'Invalid password'
		else:
			flash(user.username+' was logged in')
			#print("SHOULD BE LOGGED IN")
			#print(user.username)
			#print(user.user_id)
			#print(user.password_hash)
			#print(user.user_type)
			#print(g.user)
			session['user_id'] = user.user_id
			#print(session)
			return redirect(url_for('show_account'))
			
	#print(USER.user_id)
	return render_template('Login.html', error=error)


#-----------------------LOGOUT A USER-----------------------------#
@app.route('/logout/')
def logout():
	"""Logs the user out."""
	flash(g.user.username+' was logged out')
	session.pop('user_id', None)
	return redirect(url_for('home'))


#---------------------ACCOUNT LAYOUT FOR USERS-------------------#
@app.route('/account', methods = ['GET', 'POST'])
def show_account():
	availability = None

	if g.user.user_type == owner: #owner gets to see all events 
		schedule = all_events()
		
	elif g.user.user_type == staff: 
		availability = all_events() #should be allowed to see whats there and who signed up
		schedule = staff_events(g.user.username) #get specific staff schedule
	
	elif g.user.user_type == customer: #customer sees only events they scheduled for
		schedule = customer_events() #shown via relationship from models file
	
	else: #threw this in to have the schedule of events be shown to "guest user"
		schedule = all_events()
	return render_template('account.html', schedule=schedule, availability=availability)
	
	
#-------------------REGISTER A USER/STAFF MEMBER--------------#
@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	
	#if user signed in (aka owner) let them add a staff member
	if g.user != None and request.method == 'POST':
		if not request.form['username']:
			error = 'You Must Enter A Username'
		elif not request.form['password']:
			error = 'You Must Enter A Password'
		elif request.form['password'] != request.form['password2']:
			error = 'Your Passwords Did Not Match'
		elif get_user_id(request.form['username']) is not None:
			error = 'This Username Has Already Been Taken'
		else:
			db.session.add(USER(username=request.form['username'], password_hash=request.form['password'], user_type=staff))
			db.session.commit()
			flash('You have successfully registered this staff member')
			#print("This should be a staff member")
			#print(USER.query.all())
			return redirect(url_for('login'))
		
	#otherwise we are a customer/guest so let them be able to register for an account	
	elif request.method == 'POST':
		if not request.form['username']:
			error = 'You Must Enter A Username'
		elif not request.form['password']:
			error = 'You Must Enter A Password'
		elif request.form['password'] != request.form['password2']:
			error = 'Your Passwords Did Not Match'
		elif get_user_id(request.form['username']) is not None:
			error = 'This Username Has Already Been Taken'
		else:
			db.session.add(USER(username=request.form['username'], password_hash=request.form['password'], user_type=customer))
			db.session.commit()
			flash('You have been successfully registered and can now login')
			#print("This should be a customer")
			#print(USER.query.all())
			return redirect(url_for('login'))
			
	return render_template('Register.html', error=error)
	
	
#--------------------------SCHEDULE EVENT (CUSTOMER)-----------------#	
@app.route("/schedule_event", methods=['POST'])
def schedule_event():
	if check_date(request.form['date']):
		flash("There is an event already scheduled on this day. Please select another")
	
	else:
		db.session.add(SCHEDULING(name=request.form['name'], date=request.form['date'], customer_id=request.form['customer_id']))
		db.session.commit() #add event to database
		flash(request.form['name']+" has been created")
	
	return redirect(url_for('show_account')) #take them back to show account status


#------------------------------DELETE EVENT (CUSTOMER)-----------------#
@app.route("/delete_event", methods=['POST'])
def delete_event():
	db.session.delete(SCHEDULING.query.filter_by(event_id=request.form['event_id']).first())
	db.session.commit()
	return redirect(url_for('show_account'))
	
	
#------------------------------STAFF EVENT SIGNUP------------------------#
@app.route("/event_signup", methods=['POST'])
def event_signup():
	signupSpot = SCHEDULING.query.filter_by(event_id=request.form['event_id']).first()
	#print(signupSpot.staff1+" "+signupSpot.staff2+" "+signupSpot.staff3)

	if('staff1' in request.form):
		signupSpot.staff1 = request.form['staff1']
		
	elif('staff2' in request.form):
		signupSpot.staff2 = request.form['staff2']
		
	elif('staff3' in request.form): #should be staff spot 3, unless something terrible goes wrong
		signupSpot.staff3 = request.form['staff3']
	
	db.session.commit()
	return redirect(url_for('show_account'))	
	
# add some filters to jinja
app.jinja_env.filters['formatdatetime'] = format_datetime

if __name__ == '__main__':
    app.run()

from flask import Flask, url_for, render_template, request, redirect, jsonify, make_response, session, escape
import json
import countmeup
from countmeup import User

import pdb as debugger
from urllib2 import HTTPError
import pyrebase

app = Flask(__name__)

config = {
	"apiKey": "AIzaSyCWub-u9lHbazMA6UHtexN6vbblAfhT0sE",
	"authDomain": "count-me-up-2d6d6.firebaseapp.com",
	"databaseURL": "https://count-me-up-2d6d6.firebaseio.com",
	"storageBucket": "count-me-up-2d6d6.appspot.com",
}
#Config data for firebase

firebase = pyrebase.initialize_app(config)
#Python wrapper for firebase
auth = firebase.auth()
db = firebase.database()
app.secret_key = 'so-secret'

@app.route('/')
def index():

	results = countmeup.requestPercentageMultiProcess()
	#The application is RESTful therefore we can process the output easily
	if 'user' in session:
		#Checking if the user is logged in, if that is the case we simply keep the user auth data in session
		print "user logged in"
		print session['user'].get('email')

		return render_template('index.html',results=results,user_data=session['user'])
	else:
		print "user not logged in"

		return render_template('index.html',results=results)


@app.route('/vote',methods=['POST'])
def vote():
	user_vote_count=0
	#I chosed to keep votes on the server side and not in the session in order to ensure the vote limit cannot be broken
	if 'user' in session:
		#if the user is logged in
		email = session["user"].get("email")
		#users 'private-key'
		#debugger.set_trace()
		try:
			#just to ensure if the user selected a candidate (its always true but just in case, purely for design purposes)
			all_votes = db.child("votes").get()
			#now we get all the votes in the db
			for vote in all_votes.each():
					print(vote.key())
					print(vote.val())
					if(vote.val()["email"]==email):
						#this vote is casted by current user
						user_vote_count+=1
					#this is the total votes casted by the user in the PAST
			if user_vote_count < 3:
				vote_data = {"email":email, "vote":request.form["candidate"]}
				db.child("votes").push(vote_data)
				#we record a new vote is casted to the database.
				user_vote_count+=1
				countmeup.vote(User("anon"),request.form["candidate"])
				results = countmeup.requestPercentageMultiProcess()

				#but we compute the votes mutually exclusively from the database.
				return render_template('index.html',results=results,user_data=session['user'],message='Your vote is recorded. You have '+str(3-user_vote_count)+' votes left')
			else:
				results = countmeup.requestPercentageMultiProcess()

				return render_template('index.html',results=results,user_data=session['user'],message='Sorry, you reached your maximum vote allowance')
		except Exception, e:
			results = countmeup.requestPercentageMultiProcess()

			return render_template('index.html',results=results,user_data=session['user'],message='Please pick a candidate to vote.')

	else:
		return render_template('login.html')



@app.route('/register',methods=['POST'])
def register():
	email = request.form["email"]
	password = request.form["password"]
	try:
		#try-except is a good design choice in order to handle success/failure status of the register user-case
		user = auth.create_user_with_email_and_password(email, password)
		session['user']=user
		return redirect(url_for('index'))

	except Exception, e:
		print e
		return render_template('login.html',message='This username is already taken :(')
		pass
	#user = auth.sign_in_with_email_and_password(email, password)


@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('index'))

@app.route('/loginsuccess',methods=['POST'])
def loginsucess():
	email = request.form["email"]
	password = request.form["password"]
	try:
		user = auth.sign_in_with_email_and_password(email, password)
		session['user']=user
		#we keep the logged in users in sessions
		print session
		return redirect(url_for('index'))
	except Exception, e:
		#just to handle all sorts of exceptions and errors
		return render_template('login.html',message='wrong email/password combination')



@app.route('/fetch',methods=[ 'GET'])
def fetchResultsREST():
	#This method is for AJAX request that is executed every second. This method returns the JSON of the results.
	return jsonify(countmeup.requestPercentageMultiProcess())

if __name__ == "__main__":

		app.run(debug=True)
		app.jinja_env.globals.update(fetchResults=fetchResults)





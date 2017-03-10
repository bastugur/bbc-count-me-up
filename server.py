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


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app.secret_key = 'so-secret'

@app.route('/')
def index():

	results = countmeup.requestPercentageMultiProcess()
	if 'user' in session:
		print "user logged in"
		print session['user'].get('email')

		return render_template('index.html',results=results,user_data=session['user'])
	else:
		print "user not logged in"

		return render_template('index.html',results=results)


@app.route('/vote',methods=['POST'])
def vote():
	if 'user' in session:
		if request.form["candidate"]:
			email = session["user"].get("email")
			vote_data = {"email":email, "vote":request.form["candidate"]}
			db.child("votes").push(vote_data)
			countmeup.vote(User("someone"),request.form["candidate"])
		return redirect(url_for('index'))
	else:
		return render_template('login.html')



@app.route('/register',methods=['POST'])
def register():
	email = request.form["email"]
	password = request.form["password"]
	status=json.dumps({})
	try:
		user = auth.create_user_with_email_and_password(email, password)
		return redirect(url_for('index', status=user))

	except Exception, e:
		status = json.dumps({"status":"failed"})
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
		print session
		return redirect(url_for('index'))
	except Exception, e:
		return render_template('login.html',message='wrong email/password combination')



@app.route('/fetch',methods=[ 'GET'])
def fetchResultsREST():
	return jsonify(countmeup.requestPercentageMultiProcess())

if __name__ == "__main__":

		app.run(debug=True)
		app.jinja_env.globals.update(fetchResults=fetchResults)





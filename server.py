from flask import Flask, url_for, render_template, request, redirect, jsonify, make_response
import json
import countmeup
from countmeup import User
import pdb as debugger
app = Flask(__name__)

@app.route('/')
def index():
	results = fetchResults()
	print results
	return render_template('index.html',results=results)


@app.route('/vote',methods=[ 'POST'])
def vote():
	if request.form["candidate"]:
		print "valid request"
		countmeup.vote(User("someone"),request.form["candidate"])
	return redirect(url_for('index'))


@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/loginsuccess')
def loginsucess():
  return redirect(url_for('index'))



@app.route('/fetch',methods=[ 'GET'])
def fetchResultsREST():
  return jsonify(countmeup.requestPercentageMultiProcess())

def fetchResults():
  return countmeup.requestPercentageMultiProcess()

if __name__ == "__main__":

    app.run(debug=True)
    app.jinja_env.globals.update(fetchResults=fetchResults)





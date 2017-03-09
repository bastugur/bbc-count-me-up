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
	print request.form["name"]
	if request.form["candidate"]:
		print "valid request"
		countmeup.vote(User("someone"),request.form["candidate"])
	return redirect(url_for('index'))

@app.route('/fetch',methods=[ 'GET'])
def fetchResultsREST():
  return jsonify(countmeup.requestPercentageMultiProcess())

def fetchResults():
  return countmeup.requestPercentageMultiProcess()


def renderResults():
	return """
	    <tbody>
          <tr>
            <td>1</td>
            <td>{{results[1]}}</td>
            <td>{{100*results[1]/results.values()|sum}}%</td>
          </tr>
          <tr>
            <td>2</td>
            <td>{{results[2]}}</td>
            <td>{{100*results[2]/results.values()|sum}}%</td>
          </tr>
          <tr>
            <td>3</td>
            <td>{{results[3]}}</td>
            <td>{{100*results[3]/results.values()|sum}}%</td>
          </tr>
            <tr>
            <td>4</td>
            <td>{{results[4]}}</td>
            <td>{{100*results[4]/results.values()|sum}}%</td>
          </tr>
            <tr>
            <td>5</td>
            <td>{{results[5]}}</td>
            <td>{{100*results[5]/results.values()|sum}}%</td>
          </tr>
        </tbody>
        """
if __name__ == "__main__":

    app.run(debug=True)
    app.jinja_env.globals.update(fetchResults=fetchResults)





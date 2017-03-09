from flask import Flask, url_for, render_template, request, redirect
import countmeup
from countmeup import User

app = Flask(__name__)


@app.route("/")

@app.route('/')
def index():
	results = countmeup.main()
	print results
	return render_template('index.html',results=results)

@app.route('/vote',methods=[ 'POST'])
def vote():
	print request.form["name"]
	if request.form["candidate"]:
		print "valid request"
		countmeup.vote(User("someone"),request.form["candidate"])
	return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)


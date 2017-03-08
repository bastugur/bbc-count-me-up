from flask import Flask, url_for, render_template
import countmeup


app = Flask(__name__)


@app.route("/")

@app.route('/')
def data():
	results = countmeup.main()
	print results
	return render_template('index.html',results=results)


if __name__ == "__main__":
    app.run(debug=True)


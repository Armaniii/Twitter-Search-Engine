from flask import Flask, render_template
from elasticsearch import Elasticsearch
app = Flask(__name__)

@app.route('/')
def homepage():

    title = "EE"
    return render_template("index.html", title = title)


if __name__ == "__main__":
	app.run(debug = True, host='127.0.0.1', port=8080, passthrough_errors=True)
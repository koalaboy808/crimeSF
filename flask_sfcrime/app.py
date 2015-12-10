from flask import Flask
from flask import request, Flask, render_template, jsonify, abort, redirect


app = Flask(__name__, static_folder="public_html/static")

@app.route('/')
def load_root():
	return flask.render_template('index.html')
    # f = open('public_html/index.html', 'r')
    # raw_data = f.read()
    # return raw_data

@app.route('/<path:name>')
def load_file(name=None):
    url = 'public_html/' + name
    f = open(url, 'r')
    raw_data = f.read()
    return raw_data

if __name__ == "__main__":
    app.run()
from flask import render_template

from app import app


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/registry')
def about():
    return render_template("registry.html")

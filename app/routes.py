from flask import render_template

from app import app


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hospitals')
def hospitals():
    return render_template("registry.html")

from flask import render_template
from duvidas import app


@app.route("/")
def homepage():
    return render_template('homepage.html')

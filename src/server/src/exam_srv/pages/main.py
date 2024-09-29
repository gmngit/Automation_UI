from flask import current_app as app
from flask import request, flash, redirect, url_for, make_response
from flask import render_template
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET"])
def main_page():
    print("Visit Main Page")
    return render_template('index.html', title='Fake Hosting Service')


@app.route("/signin", methods=["GET"])
def signin_page():
    print("Visit Signin Page")
    return render_template('signin.html', title='Sign-in. Fake Hosting Service')


@app.route("/signup", methods=["GET"])
def signup_page():
    print("Visit Signup Page")
    return render_template('signup.html', title='Sign-up. Fake Hosting Service')


@app.route("/profile", methods=["GET"])
def profile_page():
    print("Visit Profile Page")
    return render_template('profile.html', title='Profile. Fake Hosting Service')

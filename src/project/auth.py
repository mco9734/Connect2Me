from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user
from .send_email import send_verification_email

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    session["email"] = email
    session["name"] = name
    session["password"] = generate_password_hash(password, method='sha256')
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # redirect to verify email
    session["tries"] = 0
    return redirect(url_for('auth.verify_email'))
    

@auth.route('/verify_email')
def verify_email():
    if session["tries"] == 0:
        session["code"] = send_verification_email(session["email"])
    if session["tries"] == 5:
        del session["tries"]
        del session["email"]
        del session["name"]
        del session["password"]
        return redirect("/")
    return render_template("verify_email.html")

@auth.route('/verify_email', methods=['POST'])
def verify_email_post():
    if request.form["code"] == session["code"]:
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=session["email"], name=session["name"], password=session["password"])
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        del session["tries"]
        del session["email"]
        del session["name"]
        del session["password"]

        return redirect(url_for('auth.login'))
    else:
        session["tries"] += 1
        return redirect(url_for("auth.verify_email"))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
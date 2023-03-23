from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from . form import LoginForm, SignupForm
from . models import User, Item
from . import db
app_auth = Blueprint('app_auth', __name__)

@app_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print('already logged in')
        flash('You are already logged in!')
        return redirect('/items')
    form = LoginForm()
    if form.validate_on_submit():
        user1 = User.query.filter_by(email=form.email.data, username=form.username.data).first()
        if user1 is not None and check_password_hash(user1.password, form.password.data):
            login_user(user1)
            return redirect("/items")
        if user1 is None:
            flash('Invalid username or email')
        elif check_password_hash(user1.password, form.password.data) == False:
            flash('Incorrect password!')
    return render_template("login.html", form=form)

@app_auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app_auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists')
            return render_template('signup.html', form=form)
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return render_template('signup.html', form=form)
        user = User(email=form.email.data, password=generate_password_hash(form.password.data), username=form.username.data)
        db.session.add(user)
        db.session.commit()
        flash('You have successfully signed-up! You can login now!')
        return redirect("/login")
    return render_template('signup.html', form=form)



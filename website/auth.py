from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.sql.functions import user
from .models import User, courseTemplate, holeTemplates
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        password = request.form.get('password')
        Action = request.form.get('Action')

        user = User.query.filter_by(first_name=firstName).first()
        if Action == 'Sign':
            return render_template("sign_up.html", User=current_user)

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('''name does not exist. If this is your first time, 
            Please sign up using the Sign Up Here button below''', category='error')

    return render_template("login.html", User=current_user)


@auth.route('/settings')
@login_required
def settings():

    return render_template("settings.html", User=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

    return f(self, *args, **kwargs)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # checks to see if the first name is valid
        user = User.query.filter_by(first_name=first_name).first()
        if user:
            flash('Name already exists', category='error')
        elif len(first_name) < 2:
            flash('firstname must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 5:
            flash('Password must be greater than 5 characters', category='error')
        else:
            # add user to database
            new_user = User(
                first_name=first_name,
                password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", User=current_user)

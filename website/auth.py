from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.sql.functions import user
from .models import User, courseTemplate, holeTemplates, currentGame, currentGameHoles
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        password = request.form.get('password')

        user = User.query.filter_by(first_name=firstName).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('name does not exist.', category='error')

    return render_template("login.html", User=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

    return f(self, *args, **kwargs)


@auth.route('/newgame')
@login_required
def newgame():
    park = 'Summit'
    course = courseTemplate.query.filter_by(parkName=park).first()
    curGame = currentGame.query.filter_by(user_id=current_user.id).first()
    if curGame:
        print(curGame.parkName)
    else:
        new_game = currentGame(
            parkName=course.parkName,
            numHoles=course.numHoles,
            curHole=1,
            user_id=current_user.id)
        db.session.add(new_game)
        for i in range(course.numHoles):
            temPar = holeTemplates.query.filter_by(user_id=current_user.id,
                        course_id=course.id, hole=i+1).first()
            new_hole = currentGameHoles(
                hole=i+1, 
                par=temPar.par,
                throws=0,
                user_id=current_user.id)

            db.session.add(new_hole)
            new_game.holes.append(new_hole)
        db.session.commit()
    curGame = currentGame.query.filter_by(user_id=current_user.id).first()
    curHole = currentGameHoles.query.filter_by(hole=curGame.curHole).first()
    if curGame.numHoles == curHole.hole :
        GameOver = True
    else:
        GameOver = False
    return render_template("newgame.html", Park=course.parkName, 
        User=current_user, hole=curGame.curHole, par=curHole.par, 
        Throws=curHole.throws, Score=curHole.throws-curHole.par, GameOver=GameOver)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

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
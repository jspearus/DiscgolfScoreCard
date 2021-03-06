from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, courseTemplate, holeTemplates
from .models import currentGame, currentGameHoles, savedGames, savedGameHoles
from . import db
import json


scorecard = Blueprint('scorecard', __name__)


@scorecard.route('/newgame', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        curGame = currentGame.query.filter_by(user_id=current_user.id).first()

        curHole = currentGameHoles.query.filter_by(user_id=current_user.id,
                                                   hole=curGame.curHole).first()

        temHole = holeTemplates.query.filter_by(user_id=current_user.id,
                                                hole=curGame.curHole, course_id=current_user.c_courseTemplate).first()
        Par = curHole.par
        hole = curGame.curHole

        btnPress = request.form.get('NavHole')
        Throws = request.form.get('throws')

        if btnPress == 'up':
            curHole.throws = curHole.throws + 1
            db.session.commit()

        elif btnPress == 'dn':
            curHole.throws = curHole.throws - 1
            if curHole.throws < 0:
                curHole.throws = 0
            db.session.commit()

        elif btnPress == 'Pre':
            hole = hole - 1
            if hole < 1:
                hole = 1
            curGame.curHole = hole
            db.session.commit()

        elif btnPress == 'Next':
            hole = hole + 1
            if hole > curGame.numHoles:
                hole = curGame.numHoles
            curGame.curHole = hole
            db.session.commit()

        elif btnPress == 'UP':
            Par = Par + 1
            curHole.par = Par
            db.session.commit()
            temHole.par = Par
            db.session.commit()

        elif btnPress == 'DN':
            Par = Par - 1
            if Par < 1:
                Par = 1
            curHole.par = Par
            db.session.commit()
            temHole.par = Par
            db.session.commit()

        elif btnPress == 'del':
            deleteCurrentGame()
            # rediects to home function in views script
            return redirect(url_for('views.home'))

        elif btnPress == 'save':
            game = currentGame.query.filter_by(user_id=current_user.id).first()
            new_game = savedGames(
                parkName=game.parkName,
                numHoles=game.numHoles,
                curHole=0,
                user_id=current_user.id)
            db.session.add(new_game)

            hole = currentGameHoles.query.filter_by(course_id=game.id,
                                                    user_id=current_user.id).all()
            for x in hole:
                new_hole = savedGameHoles(
                    hole=x.hole,
                    par=x.par,
                    throws=x.throws,
                    user_id=current_user.id)
                db.session.add(new_hole)
                new_game.holes.append(new_hole)
            db.session.commit()
            new_game = ''
            new_hole = ''
            deleteCurrentGame()
            flash('Game Saved!', category='success')
            return redirect(url_for('views.home'))
        btnPress = ''
    curScore = currentScore()
    curHole = currentGameHoles.query.filter_by(hole=curGame.curHole).first()
    if curGame.numHoles == curHole.hole and curHole.throws > 0:
        GameOver = True
    else:
        GameOver = False
    return render_template("newgame.html", Park=curGame.parkName,
                           User=current_user, hole=curGame.curHole, Throws=curHole.throws,
                           Score=curHole.throws - curHole.par, par=curHole.par, GameOver=GameOver, curScore=curScore)

# function to delete the current played game


def deleteCurrentGame():
    game = currentGame.query.filter_by(user_id=current_user.id).first()
    if game:
        if game.user_id == current_user.id:
            hole = currentGameHoles.query.filter_by(
                course_id=game.id, user_id=current_user.id).all()
            for x in hole:
                db.session.delete(x)
            db.session.delete(game)
            db.session.commit()
            game = ''
            hole = ''
    current_user.c_courseTemplate = 0
    db.session.commit()

# function to delete the current played game end

# function to calculate current score


def currentScore():
    # coode here
    tthrows = 0
    pars = 0
    hole = currentGameHoles.query.filter_by(user_id=current_user.id).all()
    for x in hole:
        pars = x.par + pars
        tthrows = x.throws + tthrows

    cScore = tthrows - pars
    return cScore


def calAvgThrows():
    game = currentGame.query.filter_by(user_id=current_user.id).first()
    temHole = holeTemplates.query.filter_by(user_id=current_user.id,
                                            hole=game.curHole,
                                            course_id=current_user.c_courseTemplate).first()
    if game:
        if game.user_id == current_user.id:
            hole = currentGameHoles.query.filter_by(
                course_id=game.id, user_id=current_user.id).all()
            for x in hole:
                new_avgThrow = holeTemplates(
                    hole=x.hole,

                )
            db.session.commit()
            game = ''
            hole = ''
    current_user.c_courseTemplate = 0
    db.session.commit()

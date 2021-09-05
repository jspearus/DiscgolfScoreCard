from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, courseTemplate, holeTemplates, currentGame, currentGameHoles, savedGames, savedGameHoles
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
                                                hole=curGame.curHole,
                                                course_id=curHole.course_id).first()

        btnPress = request.form.get('NavHole')
        Throws = request.form.get('throws')
        Par = temHole.par
        hole = curGame.curHole
       
        
        if btnPress == 'Enter':
            if ((Throws < '1')):
                flash('No Throws Entered', category='error')
                Score=0
            else:
                curHole.throws = Throws
                db.session.commit()
        elif btnPress == 'Pre':
            print ('Previous Hole')
            hole = hole - 1
            if hole < 1: hole = 1
            curGame.curHole = hole
            db.session.commit()

        elif btnPress == 'Next':
            print ('Next Hole')
            hole = hole + 1
            if hole > 7: hole = 7 
            curGame.curHole = hole
            db.session.commit()
        
        elif btnPress == 'up':
            print ('par + 1')
            Par = Par + 1
            curHole.par = Par
            db.session.commit()
            temHole.par = Par
            db.session.commit()

        elif btnPress == 'dn':
            print ('par - 1')
            Par = Par - 1
            if Par < 1: Par = 1
            curHole.par = Par
            db.session.commit()
            temHole.par = Par
            db.session.commit()

        elif btnPress == 'del':
            deleteCurrentGame()
            return render_template("home.html", User=current_user)

        elif btnPress == 'save':
            game = currentGame.query.filter_by(user_id=current_user.id).first()
            new_game = savedGames(
                parkName=game.parkName, 
                numHoles=game.numHoles,
                curHole=0, 
                user_id=current_user.id)
            db.session.add(new_game)
            
            hole = currentGameHoles.query.filter_by(course_id=game.id, user_id=current_user.id).all()
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
            new_hole=''
            deleteCurrentGame()
            flash('Game Saved!', category='success')
            return render_template("home.html", User=current_user)

    curHole = currentGameHoles.query.filter_by(hole=curGame.curHole).first()
    if curGame.numHoles == curHole.hole and curHole.throws > 0:
        GameOver = True
    else:
        GameOver = False
    return render_template("newgame.html", Park=curGame.parkName, 
                    User=current_user, hole=curGame.curHole, Throws=curHole.throws, 
                    Score=curHole.throws - curHole.par, par=curHole.par, GameOver=GameOver)

def deleteCurrentGame():
    game = currentGame.query.filter_by(user_id=current_user.id).first()
    if game:
        if game.user_id == current_user.id:
            hole = currentGameHoles.query.filter_by(course_id=game.id, user_id=current_user.id).all()
            for x in hole:
                db.session.delete(x)
            db.session.delete(game)
            db.session.commit()
            game = ''
            hole = ''
            
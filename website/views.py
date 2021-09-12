from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, courseTemplate, holeTemplates, savedGames, savedGameHoles, currentGame, currentGameHoles
from . import db
import datetime
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", User=current_user)


@views.route('/newcard', methods=['GET', 'POST'])
@login_required
def createCard():
    if request.method == 'POST':
        parkName = request.form.get('parkN')
        numHoles = request.form.get('holeN')
        nHoles = int(numHoles)
        park = courseTemplate.query.filter_by(parkName=parkName,
                                              user_id=current_user.id).first()
        if len(parkName) < 1:
            flash('note is too short', category='error')
        elif park:
            flash('Park Name Exists!')
        else:
            new_park = courseTemplate(
                parkName=parkName,
                numHoles=numHoles,
                user_id=current_user.id)
            db.session.add(new_park)

            for i in range(nHoles):
                new_hole = holeTemplates(hole=i+1, par=3,
                                         user_id=current_user.id)
                db.session.add(new_hole)
                new_park.holes.append(new_hole)
            db.session.commit()
            new_park = ''
            new_hole = ''

            flash('Card added!', category='success')
            return render_template("home.html", User=current_user)

    return render_template("newcard.html", User=current_user)


@views.route('/newgame')
@login_required
def newgame():
    curGame = currentGame.query.filter_by(user_id=current_user.id).first()
    user = current_user
    if curGame:
        pass
    else:
        course = courseTemplate.query.filter_by(
            user_id=current_user.id,
            id=user.c_courseTemplate
        ).first()
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
    if curGame.numHoles == curHole.hole:
        GameOver = True
    else:
        GameOver = False
    return render_template("newgame.html", Park=curGame.parkName,
                           User=current_user, hole=curGame.curHole, par=curHole.par,
                           Throws=curHole.throws, Score=curHole.throws-curHole.par, GameOver=GameOver)


@views.route('/games', methods=['GET', 'POST'])
@login_required
def games():
    if request.method == 'POST':
        gameid = request.form.get('Game')
        btnPress = request.form.get('delete')
        park = savedGames.query.filter_by(
            id=gameid, user_id=current_user.id).first()
        user = current_user
        if btnPress == 'DEL':
            deleteCurrentGame()
            return render_template("home.html", User=current_user)

        if park:
            user.c_SavedGame = gameid
            db.session.commit()
            Total = totalScore()
            Date = park.end_date.date()
            return render_template("gameview.html", User=current_user, game=park.parkName,
                                   date=Date.strftime("%b") + ". " + str(Date.day) + ", " + str(Date.year), savedGame=park, Total=Total)
        else:
            flash('No Game Selected', category='error')

    return render_template("games.html", User=current_user)


@views.route('/scorecards', methods=['GET', 'POST'])
@login_required
def cards():
    if request.method == 'POST':
        user = current_user
        gameid = request.form.get('Card')
        btnPress = request.form.get('Btn')
        park = courseTemplate.query.filter_by(
            id=gameid, user_id=current_user.id).first()

        if btnPress == 'DEL':
            user. c_courseTemplate = gameid
            db.session.commit()
            deleteCurrentTemp()
            return render_template("scorecards.html", User=current_user)

        if park:
            user. c_courseTemplate = gameid
            db.session.commit()
            return redirect(url_for('views.newgame'))
        else:
            flash('No Game Selected', category='error')

    return render_template("scorecards.html", User=current_user)


@views.route('/continuegame')
@login_required
def continueGame():
    user = current_user

    if user.c_courseTemplate > 0:
        return redirect(url_for('views.newgame'))
    else:
        flash('No Game Selected', category='error')
        return redirect(url_for('views.home'))


@views.route('/gameview', methods=['GET', 'POST'])
@login_required
def gameview():
    if request.method == 'POST':
        gameid = request.form.get('Game')
        park = savedGames.query.filter_by(
            id=gameid, user_id=current_user.id).first()

        if park:
            return render_template("gameview.html", User=current_user, game=park.parkName,
                                   date=park.end_date, savedGame=park)
        else:

            flash('No Game Selected', category='error')

    return render_template("games.html", User=current_user)


def deleteCurrentGame():
    user = current_user
    park = savedGames.query.filter_by(
        id=user.c_SavedGame, user_id=current_user.id).first()
    print(park)
    if park:
        if park.user_id == current_user.id:
            hole = savedGameHoles.query.filter_by(
                course_id=park.id, user_id=current_user.id).all()
            for x in hole:
                db.session.delete(x)
            db.session.delete(park)
            db.session.commit()
            park = ''
            hole = ''


def deleteCurrentTemp():
    user = current_user
    park = courseTemplate.query.filter_by(
        id=user.c_courseTemplate, user_id=current_user.id).first()
    if park:
        if park.user_id == current_user.id:
            hole = holeTemplates.query.filter_by(
                course_id=park.id, user_id=current_user.id).all()
            for x in hole:
                db.session.delete(x)
            db.session.delete(park)
            db.session.commit()
            park = ''
            hole = ''


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = courseTemplate.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            hole = holeTemplates.query.filter_by(
                course_id=note.id, user_id=current_user.id).all()
            for x in hole:
                db.session.delete(x)
            db.session.delete(note)
            db.session.commit()
            note = ''
            hole = ''
    return jsonify({})


def totalScore():
    Total = 0
    Throws = 0
    Pars = 0
    game = savedGames.query.filter_by(id=current_user.c_SavedGame,
                                      user_id=current_user.id).first()
    holes = savedGameHoles.query.filter_by(course_id=game.id,
                                           user_id=current_user.id).all()
    for x in holes:
        Throws = x.throws + Throws
        Pars = x.par + Pars
    Total = Throws - Pars

    return Total

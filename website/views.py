from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, courseTemplate, holeTemplates, savedGames, savedGameHoles
from . import db
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
        park = courseTemplate.query.filter_by(parkName=parkName, user_id=current_user.id).first()
        if len(parkName) < 1:
            flash('note is too short', category='error')
        elif park:
            flash('Park Name Exists!')
        else:
            new_park = courseTemplate(
                parkName=parkName, 
                numHoles= numHoles, 
                user_id=current_user.id)
            db.session.add(new_park)
            
            for i in range(nHoles):
                new_hole = holeTemplates(hole=i+1, par=3,
                                    user_id=current_user.id)
                db.session.add(new_hole)
                new_park.holes.append(new_hole)
            db.session.commit()
            new_park = ''
            new_hole=''

            flash('Card added!', category='success')
            return render_template("home.html", User=current_user)

    return render_template("newcard.html", User=current_user)



@views.route('/games', methods=['GET', 'POST'])
@login_required
def games():
    if request.method == 'POST':
        gameid = request.form.get('Game')
        btnPress = request.form.get('delete')
        park = savedGames.query.filter_by(id=gameid, user_id=current_user.id).first()
        user = current_user
        if btnPress == 'DEL':
            deleteCurrentGame()
            return render_template("home.html", User=current_user)

        if park:
            user.c_SavedGame = gameid
            db.session.commit()
            return render_template("gameview.html", User=current_user, game=park.parkName,
                date=park.end_date, savedGame=park)
        else:
            flash('No Game Selected', category='error')


    return render_template("games.html", User=current_user)


@views.route('/gameview', methods=['GET', 'POST'])
@login_required
def gameview():
    if request.method == 'POST':
        gameid = request.form.get('Game')
        park = savedGames.query.filter_by(id=gameid, user_id=current_user.id).first()

        if park:
            return render_template("gameview.html", User=current_user, game=park.parkName,
                date=park.end_date, savedGame=park)
        else:

            flash('No Game Selected', category='error')


    return render_template("games.html", User=current_user)

def deleteCurrentGame():
    user = current_user
    park = savedGames.query.filter_by(id=user.c_SavedGame, user_id=current_user.id).first()
    if park:
        if park.user_id == current_user.id:
            hole = savedGameHoles.query.filter_by(course_id=park.id, user_id=current_user.id).all()
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
            hole = holeTemplates.query.filter_by(course_id=note.id, user_id=current_user.id).all()
            for x in hole:
                db.session.delete(x)
            db.session.delete(note)
            db.session.commit()
            note = ''
            hole = ''
    return jsonify({})


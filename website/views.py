from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Card
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

    return render_template("home.html", user=current_user)

@views.route('/scorecard', methods=['GET', 'POST'])
@login_required
def createCard():
    if request.method == 'POST':
        parkName = request.form.get('parkN')
        numHoles = request.form.get('holeN')

        if len(parkName) < 1:
            flash('note is too short', category='error')
        else:
            new_note = Card(park=parkName, holes= numHoles, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Card added!', category='success')
            return render_template("home.html", user=current_user)

    return render_template("scorecard.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Card.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})



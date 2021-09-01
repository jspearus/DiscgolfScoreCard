from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, courseTemplate, holeTemplates
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

        if len(parkName) < 1:
            flash('note is too short', category='error')
        else:
            new_note = courseTemplate(parkName=parkName, numHoles= numHoles, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Card added!', category='success')
            return render_template("home.html", User=current_user)

    return render_template("newcard.html", User=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = courseTemplate.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})



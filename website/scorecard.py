from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, courseTemplate, holeTemplates, savedGames, savedGameHoles
from . import db
import json


scorecard = Blueprint('scorecard', __name__)

@scorecard.route('/newGame', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        Throws = request.form.get('throws')
        Par = request.form.get('par')
        print (Throws)
        print (3)
        print(int(Throws) - 3)
        Score=(int(Throws) - 3)
        
        if Throws < '1':
            flash('throws is too short', category='error')
      
            

    return render_template("newgame.html", User=current_user, Score=Score, par=3)
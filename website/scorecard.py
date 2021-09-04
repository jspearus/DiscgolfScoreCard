from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, courseTemplate, holeTemplates, savedGames, savedGameHoles
from . import db
import json


scorecard = Blueprint('scorecard', __name__)


@scorecard.route('/newgame', methods=['GET', 'POST'])
@login_required
def home():
    course = courseTemplate.query.get(1)
    if request.method == 'POST':
        btnPress = request.form.get('NavHole')
        Throws = request.form.get('throws')
        Par = request.form.get('par')
        hole = request.form.get('currentHole', type=int)
        course = courseTemplate.query.filter_by(parkName='Summit').first()

        # prints as 'none' hole and Par aren't getting values
        
        print (hole)
        print (Par)
        if btnPress == 'Enter':
            if ((Throws < '1')):
                flash('No Throws Entered', category='error')
                Score=0
            else:
                print (Throws)
                print (3)
                print(int(Throws) - 3)
                Score=(int(Throws) - 3)
        elif btnPress == 'Pre':
            print ('Previous Hole')
            hole = hole - 1
            if hole < 1: hole = 1
            Score=0

        elif btnPress == 'Next':
            print ('Next Hole')
            hole = hole + 1
            if hole > 7: hole = 7 
            Score=0
      
            

    return render_template("newgame.html", Park=course.parkName, 
                    User=current_user, hole=hole, Throws=Throws, Score=Score, par=3)
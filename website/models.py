from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

# User Table
class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150), unique=True)
    c_SavedGame = db.Column(db.Integer)
    notes = db.relationship('Note')
    courses = db.relationship('courseTemplate')
    games = db.relationship('savedGames')

# Tables for blank scorecards ###################################
class courseTemplate(db.Model):
    __tablename__ = 'courseTemplate'
    id = db.Column(db.Integer, primary_key=True)
    parkName = db.Column(db.String(140), unique=True)
    numHoles = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    holes = db.relationship('holeTemplates', backref='courseTemplate', lazy='select') 

class holeTemplates(db.Model):
    __tablename__ = 'holeTemplates'
    id = db.Column(db.Integer, primary_key=True)
    hole = db.Column(db.Integer)
    par = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('courseTemplate.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

   
# Tables For Current Game ####################################################
class currentGame(db.Model):
    __tablename__ = 'currentGame'
    id = db.Column(db.Integer, primary_key=True)
    parkName = db.Column(db.String(140) )
    numHoles = db.Column(db.Integer)
    curHole = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    holes = db.relationship('currentGameHoles', backref='currentGame', lazy='select') 

class currentGameHoles(db.Model):
    __tablename__ = 'currentGameHoles'
    id = db.Column(db.Integer, primary_key=True)
    hole = db.Column(db.Integer)
    par = db.Column(db.Integer)
    throws = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('currentGame.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

# Tables For Saved Games ####################################################
class savedGames(db.Model):
    __tablename__ = 'savedGames'
    id = db.Column(db.Integer, primary_key=True)
    parkName = db.Column(db.String(140) )
    numHoles = db.Column(db.Integer)
    curHole = db.Column(db.Integer)
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    holes = db.relationship('savedGameHoles', backref='savedGames', lazy='select') 

class savedGameHoles(db.Model):
    __tablename__ = 'savedGameHoles'
    id = db.Column(db.Integer, primary_key=True)
    hole = db.Column(db.Integer)
    par = db.Column(db.Integer)
    throws = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey('savedGames.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
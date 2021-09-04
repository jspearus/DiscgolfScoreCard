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
    notes = db.relationship('Note')
    courses = db.relationship('courseTemplate')

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

   


# Tables For Saved Games ####################################################
class savedGames(db.Model):
    __tablename__ = 'savedGames'
    id = db.Column(db.Integer, primary_key=True)
    parkName = db.Column(db.String(140) )
    numHoles = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

class savedGameHoles(db.Model):
    __tablename__ = 'savedGameHoles'
    id = db.Column(db.Integer, db.ForeignKey('savedGames.id'))
    hole = db.Column(db.Integer, primary_key=True)
    throws = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
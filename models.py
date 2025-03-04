from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, DateTime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    Id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False, unique=True)
    Password = db.Column(db.String(200), nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Qualification = db.Column(db.String(10), nullable=False)
    dob = db.Column(Date, nullable=False)
    Role = db.Column(db.String(10), nullable=False, default='user')

class Subject(db.Model):
    __tablename__ = 'subjects'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False, unique=True)
    Description = db.Column(db.String(60), nullable=True)
    chapter = db.relationship('Chapter', backref='Subject')

class Chapter(db.Model):
    __tablename__ = 'chapters'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Description = db.Column(db.String(50), nullable=True)
    Subject_id = db.Column(db.Integer, db.ForeignKey('subjects.Id'), nullable=False)
    quiz = db.relationship('Quiz', backref='Chapter')

class Quiz(db.Model):
    __tablename__ = 'quiz'
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    Chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.Id'), nullable=False)
    dateofquiz = db.Column(Date, nullable=False)
    timeduration = db.Column(db.Time, nullable=False)
    remarks = db.Column(db.String(200), nullable=True)
    questions = db.relationship('Questions', backref='Quiz')
    scores = db.relationship('Scores', backref='Quiz')

class Questions(db.Model):
    __tablename__ = 'questions'
    Id = db.Column(db.Integer, primary_key=True)
    Quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.Id'), nullable=False)
    Question = db.Column(db.String(200), nullable=False)
    Options = db.Column(db.String(300), nullable=False)
    Answer = db.Column(db.Integer, nullable = True)

class Scores(db.Model):
    __tablename__='scores'
    ID = db.Column(db.Integer, primary_key=True)
    Quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.Id'), nullable=False)
    User_id = db.Column(db.Integer, db.ForeignKey('users.Id'), nullable=False)
    Timestampofattempt = db.Column(db.DateTime, nullable=False)
    Totalscored = db.Column(db.Integer, nullable=False)
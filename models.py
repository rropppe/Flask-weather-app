from main import *


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    requests = db.relationship('Request', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime)
    user_username = db.Column(db.String(50), db.ForeignKey('user.username'))

    def __repr__(self):
        return '<Request %r>' % self.id

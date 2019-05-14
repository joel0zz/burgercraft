from application import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, username, email, password, confirmed, confirmed_on=None):
        self.username = username
        self.email = email
        self.password = password
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

    def __repr__(self):
        return '<Author {}>'.format(self.username)


from datetime import datetime

from application import db


comment_x_post = db.Table('comment_x_post',
                          db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'), primary_key=True),
                          db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    image = db.Column(db.String(36))
    slug = db.Column(db.String(255), unique=True)
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    author = db.relationship('Author',
                             backref=db.backref('posts', lazy='dynamic'))

    category = db.relationship('Category',
                               backref=db.backref('posts', lazy='dynamic'))

    comments = db.relationship('Comment', secondary=comment_x_post, lazy='subquery', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, author, title, body, image=None, category=None, slug=None, publish_date=None, live=True):
        self.author_id = author.id
        self.title = title
        self.body = body
        self.image = image
        if category:
            self.category_id = category.id
        self.slug = slug
        if publish_date is None:
            self.publish_date = datetime.utcnow()
        self.live = live

    def __repr__(self):
        return '<Post {}>'.format(self.title)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)  # query select field returns this? wtform...


class Comment(db.Model):  # post ID foreign key? need to link comments to a post..
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    comment = db.Column(db.Text)
    comment_date = db.Column(db.DateTime)

    def __init__(self, name, comment, comment_date=None):
        self.name = name
        self.comment = comment
        if comment_date is None:
            self.comment_date = datetime.utcnow()

    def __repr__(self):
        return '<Comment {}>'.format(self.comment)

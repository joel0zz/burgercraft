from flask_wtf import FlaskForm
from wtforms import validators, StringField, TextAreaField, SelectField, FileField
from flask_wtf.file import FileAllowed
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from Blog.models import Category


def categories():
    return Category.query


class PostForm(FlaskForm):
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'We only accept JPG or PNG images')
    ])
    title = StringField('Title', validators=[
            validators.InputRequired(),
            validators.Length(max=80)
        ])
    body = TextAreaField('Content', validators=[validators.InputRequired()])
    category = QuerySelectField('Category', query_factory=categories,
                                allow_blank=True)
    new_category = StringField('New Category')


class CommentForm(FlaskForm):
    comment = TextAreaField('Your Comment', validators=[validators.InputRequired()])


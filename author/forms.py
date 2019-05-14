from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField
from werkzeug.security import check_password_hash

from author.models import Author


class LoginForm(FlaskForm):
    email = EmailField('Email Address', [validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8, max=80)
    ])

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        author = Author.query.filter_by(
            email=self.email.data
        ).first()

        if author:
            if not check_password_hash(author.password, self.password.data):
                self.password.errors.append('Incorrect email or password')
                return False
            return True
        else:
            self.password.errors.append('Incorrect email or password')


class RegisterForm(FlaskForm):
    username = StringField('User Name', [validators.InputRequired()])
    email = EmailField('Email Address', [validators.InputRequired(), validators.Email(message="Please enter a valid Email.")])
    password = PasswordField('New Password', [
        validators.InputRequired(),
        validators.Length(min=8, max=80)
        ])
    confirm = PasswordField('Repeat Password', [
        validators.EqualTo('password', message='Password must match'),
        ])

    # custom validators -- name of method must be validate_"formfield" -- These check for duplicate email/username's
    # they don't need to be called from anywhere -- wtforms handles everything.
    def validate_email(self, email):
        author = Author.query.filter_by(email=email.data).first()
        if author is not None:
            raise ValidationError('Email already in use, please use a different one.')

    def validate_username(self, username):
        author = Author.query.filter_by(username=username.data).first()
        if author is not None:
            raise ValidationError('Username is already in use, please use a different one.')


class SendPasswordResetForm(FlaskForm):
    email = StringField("Email Address", [validators.InputRequired(), validators.Email(message="Please enter a valid Email.")])


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', [
        validators.InputRequired(),
        validators.Length(min=8, max=80)
    ])
    confirm = PasswordField('Repeat Password', [
        validators.EqualTo('password', message='Password must match'),
    ])


class ChangeUsernameForm(FlaskForm):
    username = StringField('User Name', [validators.InputRequired()])

    def validate_username(self, username):
        author = Author.query.filter_by(username=username.data).first()
        if author is not None:
            raise ValidationError('Username is already in use, please use a different one.')
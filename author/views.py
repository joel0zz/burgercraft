from flask import Blueprint, render_template, redirect, session, url_for, flash, request
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import datetime
from threading import Thread
from rq import Queue

author_app = Blueprint('author_app', __name__)

from application import db, create_app
from author.models import Author
from author.forms import RegisterForm, LoginForm, SendPasswordResetForm, ResetPasswordForm
from author.decorators import login_required, already_logged_in
from worker import conn


q = Queue(connection=conn)
application = create_app()
mail = Mail(application)


@author_app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        author = Author(
            form.username.data,
            form.email.data,
            hashed_password,
            confirmed=False
        )
        db.session.add(author)
        db.session.commit()

        token = generate_confirmation_token(author.email)
        confirm_url = url_for('.confirm_email', token=token, _external=True)
        html = render_template('author/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(author.email, subject, html)
        flash('A confirmation email has been sent, please check your inbox.', 'success')
        return redirect(url_for('.login'))

    return render_template('author/register.html', form=form)


@author_app.route('/login', methods=('GET', 'POST'))
@already_logged_in
def login():
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)

    if form.validate_on_submit():
        author = Author.query.filter_by(email=form.email.data).first()
        session['id'] = author.id
        session['username'] = author.username
        if 'next' in session:
            next = session.get('next')
            session.pop('next')
            return redirect(next)
        else:
            flash(f"Welcome {author.username}.", "success")
            return redirect(url_for('blog_app.index'))

    return render_template('author/login.html', form=form, error=error)


@author_app.route('/send_password_reset', methods=["GET", "POST"])
@already_logged_in
def send_password_reset():
    form = SendPasswordResetForm()
    flash('Please enter your email address', 'info')

    if form.validate_on_submit():
        author = Author.query.filter_by(email=form.email.data).first()
        if author:
            token = generate_confirmation_token(author.email)
            confirm_url = url_for('.reset_password', token=token, _external=True)
            html = render_template('author/reset_email.html', confirm_url=confirm_url)
            subject = "Password Reset"
            q.enqueue(send_email, args=(author.email, subject, html))

            flash("Thanks, please check your inbox for instructions.", "success")
            return redirect(url_for('.login'))

    return render_template('author/send_password_reset.html', form=form)


@author_app.route('/reset_password/<token>', methods=['GET', 'POST'])
@already_logged_in
def reset_password(token):
    email = confirm_token(token)  # de-serialize the token to retrieve email.
    form = ResetPasswordForm()
    author = Author.query.filter_by(email=email).first_or_404()  # retrieve author using email.
    if email is False:
        flash('The reset link is invalid or has expired, please request another one', 'error')  # check for expired tokens.
        return redirect(url_for('.login'))
    flash(f'Hi {author.username}, please enter a new password.', 'info')
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)  # generate hash from pass form data.
        author.password = hashed_password  # change authors password
        db.session.commit()
        flash("Password successfully reset.", "success")
        return redirect(url_for('.login'))
    return render_template('author/reset_password.html', form=form)


@author_app.route('/logout')
def logout():
    session.pop('id')
    session.pop('username')
    flash('User logged out.', 'success')
    return redirect(url_for('.login'))


@author_app.route('/confirm/<token>')  # users will click unique link, which will pass the token into this view.
def confirm_email(token):
    email = confirm_token(token)  # call confirm function, to retrieve email or False.
    if email is False:
        flash('The confirmation link is invalid or has expired.', 'error')
        return redirect(url_for('blog_app.unconfirmed'))
    author = Author.query.filter_by(email=email).first_or_404()  # query the Author model, searching via email.
    if author.confirmed:
        flash("Account already confirmed.", "success")  # <---- already confirmed message.
    else:
        #  set DB fields confirmed & confirmed on, if user is not yet confirmed.
        author.confirmed = True
        author.confirmed_on = datetime.datetime.now()
        db.session.add(author)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')  # <-- success
    return redirect(url_for('blog_app.index'))  # redirect to index.


@author_app.route('/resend')
@login_required
def resend_confirmation():
    author = Author.query.get(session['id'])
    token = generate_confirmation_token(author.email)
    confirm_url = url_for('.confirm_email', token=token, _external=True)
    html = render_template('author/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(author.email, subject, html)
    flash('A new confirmation email has been sent, please check your inbox.', 'success')
    return redirect(url_for('blog_app.unconfirmed'))


@author_app.route('/profile')
def profile():
    return "profile here"


# generate unique token using users email & secret key / password salt in os.environ
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(application.config['SECRET_KEY'])
    return serializer.dumps(email, salt=application.config['SECURITY_PASSWORD_SALT'])


# pass the token into the serializer to retrieve the users email address or False, if nothing found.
def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(application.config['SECRET_KEY'])
    try:
        email = serializer.loads(token,
                                 salt=application.config['SECURITY_PASSWORD_SALT'],
                                 max_age=expiration)
    except:
        return False
    return email


# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=application.config['MAIL_DEFAULT_SENDER']
    )
    #Thread(target=send_async_email, args=(application, msg)).start()  # creates a job to send the email.
    mail.send(msg)


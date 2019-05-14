from functools import wraps
from flask import session, request, redirect, url_for, abort, flash

from author.models import Author


#  Decorator to handle login/confirmation checks. This will be used in multiple views.
def login_required_check_confirmed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('id') is None:  # if no user session, redirect to login page. First check.
            flash('Please login to continue.', 'error')
            return redirect(url_for('author_app.login', next=request.url))
        if (Author.query.get(session['id'])).confirmed is False:  # if user.confirmed field is 0 (false) -> redirect.
            flash("Account not confirmed.", 'error')
            return redirect(url_for('blog_app.unconfirmed'))
        return f(*args, **kwargs)
    return decorated_function


#  Some views only require a login check.
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('id') is None:
            flash('Please login to continue.', 'error')
            return redirect(url_for('author_app.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def already_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('id'):
            flash("You're already logged in.", 'success')
            return redirect(url_for('blog_app.index'))
        return f(*args, **kwargs)
    return decorated_function
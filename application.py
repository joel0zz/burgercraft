from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown
import os

# setup db
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    application = Flask(__name__)

    # load config
    #application.config.from_pyfile('config/config.py')
    application.config.from_mapping(
        BLOG_NAME=os.environ.get('BLOG_NAME'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        SECURITY_PASSWORD_SALT=os.environ.get('SECURITY_PASSWORD_SALT'),
        DB_USERNAME=os.environ.get('DB_USERNAME'),
        DB_PASSWORD=os.environ.get('DB_PASSWORD'),
        DB_HOST=os.environ.get('DB_HOST'),
        DATABASE_NAME=os.environ.get('DATABASE_NAME'),
        #DATABASE_URL=os.environ.get('DATABASE_URL'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

        MAIL_SERVER=os.environ.get('MAIL_SERVER'),
        MAIL_PORT=os.environ.get('MAIL_PORT'),
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER'),
        MAIL_USE_TLS=True,
        MAIL_USE_SSL=False,

        BUCKET_NAME=os.environ.get('BUCKET_NAME'),
        REGION=os.environ.get('REGION')
    )

    # initialize db
    db.init_app(application)
    migrate.init_app(application, db)

    # Markdown
    Markdown(application)

    # import blueprints
    from Blog.views import blog_app
    from author.views import author_app

    # register blueprints
    application.register_blueprint(blog_app)
    application.register_blueprint(author_app)

    return application



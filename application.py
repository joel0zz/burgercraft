from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flaskext.markdown import Markdown



# setup db
db = SQLAlchemy()

application = Flask(__name__)

# load config
application.config.from_pyfile('config.py')

# initialize db
db.init_app(application)
migrate = Migrate(application, db)

# Markdown
Markdown(application)

# import blueprints
from Blog.views import blog_app
from author.views import author_app

# register blueprints
application.register_blueprint(blog_app)
application.register_blueprint(author_app)

if __name__ == "__main__":
    application.run()
    db.session.rollback()

import os
import unittest
import pathlib
from flask import session
from slugify import slugify

from dotenv import load_dotenv
env_dir = pathlib.Path(__file__).parents[1]
load_dotenv(os.path.join(env_dir, '.env'))


from app import db
from app import create_app as create_app_base
from utils.test_db import TestDB


class PostTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(
            SQLALCHEMY_DATABASE_URI=self.db_uri,
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY='mySecret!'
        )

    def setUp(self):
        self.test_db = TestDB()
        self.db_uri = self.test_db.create_db()
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()
        with self.app_factory.app_context():
            db.create_all()

    def tearDown(self):
        with self.app_factory.app_context():
            db.drop_all()
        self.test_db.drop_db()

    def user_dict(self):
        return dict(
            username='John Smith',
            email='jsmith@example.com',
            password='test123555',
            confirm='test123555'
        )

    def post_dict(self):
        return dict(
            title='My Awesome Post',
            body='This is my awesome post content',
            new_category='Tech'
        )

    def test_blog_post_create(self):
        # Post without logging in
        rv = self.app.get('/post', follow_redirects=True)
        assert 'Please login to continue' in str(rv.data)

        # Register and login
        rv = self.app.post('/register', data=self.user_dict())
        rv = self.app.post('/login', data=self.user_dict())

        # post first post
        rv = self.app.post('/post', data=self.post_dict(),
                           follow_redirects=True)
        assert 'Article Posted' in str(rv.data)
        assert 'Tech' in str(rv.data) # category
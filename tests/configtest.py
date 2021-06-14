import os
import string
import tempfile
import random

import pytest
import unittest

from app import create_app
from app.data import db as _db

@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    application = create_app()

    # Establish an application context before running the tests.
    ctx = application.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return application


@pytest.fixture(scope='module')
def db(app, request):
    """Session-wide test database."""
    _db.app = app

    # wipe postgres
    _db.drop_all()
    # recreate postgres
    _db.create_all()

    return _db


@pytest.fixture(scope='module')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(autoflush=False, expire_on_commit=False)
    session = db.create_scoped_session(options)
    db.session = session

    request.addfinalizer(transaction.rollback)
    request.addfinalizer(connection.close)
    request.addfinalizer(session.remove)

    return session

@pytest.fixture(scope='session')
def client(app, request):
    return app.test_client()


def auth_header(token):
    return [('Authorization', 'Token {}'.format(token))]


def random_char(y):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(y))


class BaseTest(object):

    def setUp(self):
        pass

    def tearDown(self):
        pass

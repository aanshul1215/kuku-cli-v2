from __future__ import annotations

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import pytest
from app import create_app
from app.config import TestConfig
from app.db import db
from app.models import User

@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            _populate_database()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture(scope='function')
def db_session(client):
    yield db.session

def _populate_database():
    admin_user = User(username='admin', password='admin', firstname='Admin', lastname='User', balance=1000.00)
    db.session.add(admin_user)
    db.session.commit()

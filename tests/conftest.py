import os
import tempfile
import pytest
from database import create_app, create_db


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def db():
    db = create_db(app())
    return db


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db(app)
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

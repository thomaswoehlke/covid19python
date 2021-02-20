import os
import tempfile
import pytest
from database import create_app_test, create_db


@pytest.fixture
def app():
    app = create_app_test()
    return app


@pytest.fixture
def client():
    app = create_app_test()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            create_db(app)
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

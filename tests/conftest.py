import os
import tempfile
import pytest
from database import create_app, create_db_test, create_admin

pytest_plugins = ("celery.contrib.pytest", )


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client():
    app = create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            create_db_test(app)
            create_admin(app)
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

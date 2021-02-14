from celery.contrib import pytest

from database import app, run_run_with_debug, port
import covid19.blueprints.application.application_views

@pytest.fixture
def test_app():
    my_test_app = app
    return my_test_app

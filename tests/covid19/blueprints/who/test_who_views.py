import pytest
from flask import url_for
import covid19.blueprints.application.application_views
import tests.conftest

appctx = None
reqctx = None


def test_url_admin_tasks(client):
    url = url_for(endpoint='who.url_who_info', _external=True, appctx=appctx, reqctx=reqctx)
    assert client.get(url).status_code == 200


def test_url_admin_info(client):
    url = url_for(endpoint='who.url_who_info', _external=True, appctx=appctx, reqctx=reqctx)
    assert client.get(url).status_code == 200

from celery.contrib import pytest

from database import app, run_run_with_debug, port
import covid19.blueprints.application.application_views

from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger
import conftest
import src.covid19.blueprints.who.who_views

from celery.contrib import pytest


@pytest.mark.usefixtures('live_server')
class TestLiveServer:

    def test_url_admin_tasks(client):
        assert client.get(url_for('who.url_who_tasks')).status_code == 200

    def test_url_admin_info(client):
        assert client.get(url_for('who.url_who_info')).status_code == 200

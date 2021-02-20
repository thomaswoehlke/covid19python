from flask import render_template, redirect, url_for, flash, Blueprint
from celery import states
from celery.utils.log import get_task_logger
import conftest


def test_url_admin_tasks(client):
    assert client.get(url_for('admin.url_admin_tasks')).status_code == 200


def test_url_admin_info(client):
    assert client.get(url_for('admin.url_admin_info')).status_code == 200


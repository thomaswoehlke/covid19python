from database import app, run_run_with_debug, port
import covid19
import covid19.blueprints.application.application_views

from covid19 import run_web

# https://realpython.com/pytest-python-testing/
# https://www.guru99.com/pytest-tutorial.html
#
#
# https://docs.pytest.org/en/stable/
# https://www.jetbrains.com/help/pycharm/pytest.html
# https://docs.celeryproject.org/en/stable/userguide/testing.html
#
# https://werkzeug.palletsprojects.com/en/1.0.x/test/#werkzeug.test.Client
# https://flask.palletsprojects.com/en/1.1.x/testing/
# https://flask.palletsprojects.com/en/1.1.x/tutorial/tests/
#
# https://flask.palletsprojects.com/en/1.1.x/tutorial/install/
# https://packaging.python.org/tutorials/packaging-projects/


# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == '__main__':
    run_web()

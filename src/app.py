import sys
import subprocess
import covid19
import covid19_worker
from covid19.blueprints.application.application_workers import app, run_app, celery

# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == '__main__':
    run_app(app)

from database import app, run_run_with_debug, port
import covid19
import covid19.blueprints.application.application_views

from covid19 import run_web

# ---------------------------------------------------------------------------------
#  MAIN
# ---------------------------------------------------------------------------------

if __name__ == '__main__':
    run_web()

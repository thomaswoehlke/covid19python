from database import app, run_run_with_debug, port

import covid19.blueprints.application.application_views


def run_web():
    app.logger.info(" ")
    app.logger.info("#############################################################")
    app.logger.info("#                Covid19 Data - WEB                         #")
    app.logger.info("#############################################################")
    app.logger.info(" ")
    app.run(debug=run_run_with_debug, port=port)


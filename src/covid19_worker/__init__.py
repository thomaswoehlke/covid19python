import sys
import subprocess
from covid19 import app
from covid19.blueprints.application.application_workers import celery


def run_mq():
    app.logger.info(" ")
    app.logger.info("#############################################################")
    app.logger.info("#                Covid19 Data - WORKER                      #")
    app.logger.info("#############################################################")
    app.logger.info(" ")
    if sys.platform != 'linux':
        redis_cmd = ['redis-server']
        subprocess.Popen(redis_cmd, shell=True)
    args = ['worker', '-l', 'INFO']
    celery.start(args)

import sys
import subprocess
from covid19 import app
from database import create_celery


def run_mq(my_app, my_celery):
    if sys.platform != 'linux':
        my_app.logger.info("-------------------------------------------------------------")
        my_app.logger.info("#                start REDIS-Server                         #")
        my_app.logger.info("-------------------------------------------------------------")
        redis_cmd = ['redis-server']
        subprocess.Popen(redis_cmd, shell=True)
    my_app.logger.info(" ")
    my_app.logger.info("#############################################################")
    my_app.logger.info("#                Covid19 Data - WORKER                      #")
    my_app.logger.info("#############################################################")
    my_app.logger.info(" ")
    args = ['worker', '-l', 'INFO']
    my_celery.start(args)


celery = create_celery(app)

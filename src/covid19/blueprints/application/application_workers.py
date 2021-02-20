import sys
import subprocess
from covid19 import app
from database import create_celery, run_run_with_debug, port


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


def run_app(my_app):
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
    celery_cmd = ['celery', 'worker', '-l', 'INFO']
    subprocess.Popen(celery_cmd, shell=True)
    my_app.logger.info(" ")
    my_app.logger.info("#############################################################")
    my_app.logger.info("#                Covid19 Data - WEB                         #")
    my_app.logger.info("#############################################################")
    my_app.logger.info(" ")
    my_app.run(
        debug=run_run_with_debug,
        port=port
    )


celery = create_celery(app)

from app import app
from workers import celery

#################################################################################################################
#
# MAIN
#
#################################################################################################################
if __name__ == '__main__':
    app.logger.info(" ")
    app.logger.info("#############################################################")
    app.logger.info("#                Covid19 Data - WORKER                      #")
    app.logger.info("#############################################################")
    app.logger.info(" ")
    args = ['worker', '-l', 'INFO']
    celery.start(args)

#!/user/bin/env python

import os
import sys
import subprocess
import logging
from setuptools import setup, find_packages


def get_python_requirements_from_txt():
    my_cmd = ['bash', 'scripts'+os.sep+'scipt_get_python_requirements_from_txt.sh']
    returncode = subprocess.call(my_cmd, shell=True)
    if returncode == 0:
        logging.info("retcode: "+str(returncode))
    else:
        logging.error("retcode: " + str(returncode))
    return None


get_python_requirements_from_txt()

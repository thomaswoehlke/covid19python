#!/user/bin/env python

import os
import sys
import subprocess
import logging
from setuptools import setup, find_packages


def run_npm_install():
    my_cmd = ['npm', 'install']
    returncode = subprocess.call(my_cmd, shell=True)
    if returncode == 0:
        logging.info("retcode: "+str(returncode))
    else:
        logging.error("retcode: " + str(returncode))
    return None


run_npm_install()

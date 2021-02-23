#!/user/bin/env python

import os
import sys
import subprocess
import logging
from setuptools import setup, find_packages


def run_compile_requirements():
    my_cmd_list = [
        ['pip-compile', '-r', 'requirements' + os.sep + 'build.in'],
        ['pip-compile', '-r', 'requirements' + os.sep + 'docs.in'],
        ['pip-compile', '-r', 'requirements' + os.sep + 'tests.in'],
        ['pip-compile', '-r', 'requirements' + os.sep + 'dev.in'],
        ['pip', 'install', '-r', 'requirements' + os.sep + 'build.in'],
        ['pip', 'install', '-r', 'requirements' + os.sep + 'docs.in'],
        ['pip', 'install', '-r', 'requirements' + os.sep + 'tests.in'],
        ['pip', 'install', '-r', 'requirements' + os.sep + 'dev.in'],
    ]
    for my_cmd in my_cmd_list:
        returncode = subprocess.call(my_cmd, shell=True)
        if returncode == 0:
            logging.info("retcode: "+str(returncode))
        else:
            logging.error("retcode: " + str(returncode))
    return None


run_compile_requirements()

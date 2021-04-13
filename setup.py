import os
import sys
import logging
import subprocess

from setuptools import find_packages, setup

version = '0.0.28'

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

readme = open("README.md").read()
history = open("docs" + os.sep + "BACKLOG.md").read()

keywords_list = [
    "virus",
    "pandemic",
    "covid19",
    "corona",
    "who",
    "rki",
    "ecdc",
    "deaths",
    "cases",
    "vaccination",
    "data",
    "statistic",
    "python",
    "flask",
    "celery",
    "sqlalchemy",
    "postgresql"
]

requires_build = [
	"appdirs==1.4.4",
	"argparse==1.4.0",
	"bleach==3.3.0",
	"build==0.3.1.post1",
	"certifi==2020.12.5",
	"cffi==1.14.5",
	"cfgv==3.2.0",
	"chardet==3.0.4",
	"click==7.1.2",
	"colorama==0.4.4",
	"cryptography==3.4.7",
	"distlib==0.3.1",
	"docutils==0.17",
	"filelock==3.0.12",
	"identify==1.5.14",
	"idna==2.10",
	"importlib-metadata==3.10.0",
	"jeepney==0.6.0",
	"keyring==23.0.1",
	"nodeenv==1.5.0",
	"packaging==20.9",
	"pbr==3.1.1",
	"pep517==0.10.0",
	"pip-licenses==3.3.0",
	"pip-tools==5.5.0",
	"pipenv==2020.11.15",
	"pkginfo==1.7.0",
	"pre-commit==2.10.1",
	"ptable==0.9.2",
	"py==1.10.0",
	"pyaml==20.4.0",
	"pycparser==2.20",
	"pygments==2.8.1",
	"pyparsing==2.4.7",
	"python-dotenv==0.15.0",
	"python-magic==0.4.22",
	"pytoolbox==14.0.0",
	"pytz==2021.1",
	"pyyaml==5.4.1",
	"readme-renderer==29.0",
	"requests-toolbelt==0.9.1",
	"requests==2.25.1",
	"rfc3986==1.4.0",
	"secretstorage==3.3.1",
	"six==1.15.0",
	"toml==0.10.2",
	"tqdm==4.59.0",
	"twine==3.4.1",
	"urllib3==1.26.4",
	"venv-run==0.1.0",
	"virtualenv-clone==0.5.4",
	"virtualenv==20.4.3",
	"webencodings==0.5.1",
	"wheel==0.36.2",
	"zipp==3.4.1",
]

requires_test = [
	"alembic==1.5.5",
	"appdirs==1.4.4",
	"attrs==20.3.0",
	"click==7.1.2",
	"distlib==0.3.1",
	"filelock==3.0.12",
	"flask-db==0.3.1",
	"flask-fixtures==0.3.8",
	"flask-sqlalchemy==2.4.4",
	"flask==1.1.2",
	"iniconfig==1.1.1",
	"itsdangerous==1.1.0",
	"jaraco.context==4.0.0",
	"jaraco.functools==3.2.1",
	"jinja2==2.11.3",
	"mako==1.1.4",
	"markupsafe==1.1.1",
	"mirakuru==2.3.0",
	"more-itertools==8.7.0",
	"packaging==20.9",
	"pluggy==0.13.1",
	"port-for==0.4",
	"psutil==5.8.0",
	"py==1.10.0",
	"pyparsing==2.4.7",
	"pytest-enabler==1.2.0",
	"pytest-flask-sqlalchemy==1.0.2",
	"pytest-flask==1.2.0",
	"pytest-mock==3.5.1",
	"pytest-postgresql==2.6.1",
	"pytest-runner==5.3.0",
	"pytest-venv==0.2.1",
	"pytest==6.2.3",
	"python-dateutil==2.8.1",
	"python-editor==1.0.4",
	"six==1.15.0",
	"sqlalchemy-utils==0.36.8",
	"sqlalchemy==1.3.23",
	"toml==0.10.2",
	"urllib3==1.26.4",
	"virtualenv==20.4.2",
	"werkzeug==1.0.1",
]

requires_docs = [
    	"alabaster==0.7.12",
	"babel==2.9.0",
	"certifi==2020.12.5",
	"cffi==1.14.5",
	"chardet==3.0.4",
	"cryptography==3.4.7",
	"docutils==0.16",
	"github3.py==2.0.0",
	"httplib2==0.19.0",
	"idna==2.10",
	"imagesize==1.2.0",
	"jinja2==2.11.3",
	"jwcrypto==0.8",
	"markdown==3.3.3",
	"markupsafe==1.1.1",
	"packaging==20.0",
	"pbr==5.5.1",
	"plantuml-gentools==0.1.2",
	"plantuml-markdown==3.4.2",
	"plantuml-wrapper==0.1.0",
	"plantuml==0.3.0",
	"py2puml==0.4.0",
	"pycparser==2.20",
	"pygments==2.8.0",
	"pyparsing==2.4.7",
	"python-dateutil==2.8.1",
	"pytz==2021.1",
	"requests==2.25.1",
	"six==1.13.0",
	"snowballstemmer==2.1.0",
	"speaklater==1.3",
	"sphinx==3.4.3",
	"sphinxcontrib-applehelp==1.0.2",
	"sphinxcontrib-devhelp==1.0.2",
	"sphinxcontrib-github==0.1.3",
	"sphinxcontrib-gravizo==0.0.4",
	"sphinxcontrib-htmlhelp==1.0.3",
	"sphinxcontrib-jsmath==1.0.1",
	"sphinxcontrib-log-cabinet==1.0.1",
	"sphinxcontrib-plantuml==0.20.1",
	"sphinxcontrib-qthelp==1.0.3",
	"sphinxcontrib-serializinghtml==1.1.4",
	"tokenize-rt==4.1.0",
	"uritemplate==3.0.1",
	"urllib3==1.26.4",
]

dotenv_require = [
    "python-dotenv==0.15.0"
]

requires_extras = {
    "docs": requires_docs,
    "tests": requires_test,
    "dotenv": dotenv_require,
    "all": []
}

requires_dev = [
	"alabaster==0.7.12",
	"alembic==1.5.4",
	"amqp==5.0.5",
	"appdirs==1.4.4",
	"argparse==1.4.0",
	"attrs==19.3.0",
	"babel==2.9.0",
	"billiard==3.6.3.0",
	"bleach==3.3.0",
	"blinker==1.4",
	"build==0.3.1.post1",
	"celery[redis]==5.0.5",
	"certifi==2020.12.5",
	"cffi==1.14.5",
	"cfgv==3.2.0",
	"chardet==3.0.4",
	"click-didyoumean==0.0.3",
	"click-plugins==1.1.1",
	"click-repl==0.1.6",
	"click==7.1.2",
	"colorama==0.4.4",
	"cryptography==3.4.7",
	"cycler==0.10.0",
	"distlib==0.3.1",
	"docutils==0.16",
	"dominate==2.6.0",
	"filelock==3.0.12",
	"flask-admin==1.5.7",
	"flask-babel==2.0.0",
	"flask-bs4==5.0.0.1",
	"flask-cors==3.0.10",
	"flask-db==0.3.1",
	"flask-fixtures==0.3.8",
	"flask-pluginkit==3.6.0",
	"flask-redisboard==0.2.0",
	"flask-sqlalchemy==2.5.1",
	"flask-whooshalchemy3==0.2.0",
	"flask-wtf==0.14.3",
	"flask==1.1.2",
	"github3.py==2.0.0",
	"greenlet==1.0.0",
	"httplib2==0.19.0",
	"identify==1.5.13",
	"idna==2.10",
	"imagesize==1.2.0",
	"importlib-metadata==3.10.0",
	"iniconfig==1.1.1",
	"itsdangerous==1.1.0",
	"jaraco.context==4.0.0",
	"jaraco.functools==3.2.1",
	"jeepney==0.6.0",
	"jinja2==2.11.3",
	"joblib==1.0.1",
	"jsonpatch==1.28",
	"jsonpointer==2.0",
	"jwcrypto==0.8",
	"keyring==23.0.1",
	"kiwisolver==1.3.1",
	"kombu==5.0.2",
	"llvmlite==0.35.0",
	"mako==1.1.4",
	"markdown==3.3.3",
	"markupsafe==1.1.1",
	"matplotlib==3.3.4",
	"mirakuru==2.3.0",
	"more-itertools==8.0.2",
	"nodeenv==1.5.0",
	"numba==0.52.0",
	"numpy==1.20.2",
	"packaging==20.9",
	"pandas==1.2.3",
	"pbr==3.1.1",
	"pep517==0.10.0",
	"pillow==8.2.0",
	"pip-licenses==3.3.0",
	"pip-tools==5.5.0",
	"pipenv==2020.11.15",
	"pkginfo==1.7.0",
	"plantuml-gentools==0.1.2",
	"plantuml-markdown==3.4.2",
	"plantuml-wrapper==0.1.0",
	"plantuml==0.3.0",
	"pluggy==0.13.1",
	"port-for==0.4",
	"pre-commit==2.10.1",
	"prettytable==2.0.0",
	"prompt-toolkit==3.0.16",
	"psutil==5.8.0",
	"psycopg2-binary==2.8.6",
	"ptable==0.9.2",
	"py2puml==0.4.0",
	"py==1.10.0",
	"pyaml==20.4.0",
	"pycparser==2.20",
	"pyecharts-extras==0.0.5",
	"pyecharts==1.9.0",
	"pygments==2.8.0",
	"pynndescent==0.5.2",
	"pyparsing==2.4.7",
	"pytest-enabler==1.2.0",
	"pytest-flask-sqlalchemy==1.0.2",
	"pytest-flask==1.2.0",
	"pytest-mock==3.5.1",
	"pytest-postgresql==2.6.1",
	"pytest-runner==5.3.0",
	"pytest-venv==0.2.1",
	"pytest==6.2.3",
	"python-dateutil==2.8.1",
	"python-dotenv==0.15.0",
	"python-editor==1.0.4",
	"python-magic==0.4.22",
	"pytoolbox==14.0.0",
	"pytz==2020.5",
	"pyyaml==5.4.1",
	"pyzmq==22.0.3",
	"readme-renderer==29.0",
	"redis==3.5.3",
	"requests-toolbelt==0.9.1",
	"requests==2.25.1",
	"rfc3986==1.4.0",
	"scikit-learn==0.24.1",
	"scipy==1.6.2",
	"secretstorage==3.3.1",
	"semver==2.13.0",
	"simplejson==3.17.2",
	"six==1.15.0",
	"snowballstemmer==2.1.0",
	"speaklater==1.3",
	"sphinx==3.4.3",
	"sphinxcontrib-applehelp==1.0.2",
	"sphinxcontrib-devhelp==1.0.2",
	"sphinxcontrib-github==0.1.3",
	"sphinxcontrib-gravizo==0.0.4",
	"sphinxcontrib-htmlhelp==1.0.3",
	"sphinxcontrib-jsmath==1.0.1",
	"sphinxcontrib-log-cabinet==1.0.1",
	"sphinxcontrib-plantuml==0.20.1",
	"sphinxcontrib-qthelp==1.0.3",
	"sphinxcontrib-serializinghtml==1.1.4",
	"sqlalchemy-utils==0.36.8",
	"sqlalchemy==1.4.5",
	"statisticaldiagrams==20.5",
	"threadpoolctl==2.1.0",
	"tokenize-rt==4.1.0",
	"toml==0.10.2",
	"torch==1.8.1",
	"torchfile==0.1.0",
	"tornado==6.1",
	"tqdm==4.59.0",
	"twine==3.4.1",
	"typing-extensions==3.7.4.3",
	"uritemplate==3.0.1",
	"urllib3==1.26.4",
	"venv-run==0.1.0",
	"vine==5.0.0",
	"virtualenv-clone==0.5.4",
	"virtualenv==20.4.3",
	"visdom==0.1.8.9",
	"visitor==0.1.3",
	"wcwidth==0.1.8",
	"webencodings==0.5.1",
	"websocket-client==0.57.0",
	"werkzeug==1.0.1",
	"wget==3.2",
	"wheel==0.36.2",
	"whoosh==2.7.4",
	"wtforms==2.3.3",
	"zipp==3.4.1",
] + pytest_runner


for reqs in requires_extras.values():
    requires_extras["all"].extend(reqs)

keywords = ""
for kw in keywords_list:
    keywords += " " + kw

packages = find_packages()


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


def run_npm_install():
    my_cmd = ['npm', 'install']
    returncode = subprocess.call(my_cmd, shell=True)
    if returncode == 0:
        logging.info("retcode: "+str(returncode))
    else:
        logging.error("retcode: " + str(returncode))
    return None


def get_python_requirements_from_txt():
    my_cmd = ['bash', 'scripts'+os.sep+'script_get_python_requirements_from_txt.sh']
    returncode = subprocess.call(my_cmd, shell=True)
    if returncode == 0:
        logging.info("retcode: "+str(returncode))
    else:
        logging.error("retcode: " + str(returncode))
    return None


setup(
    name='flask-covid19',
    version=version,
    url='https://github.com/thomaswoehlke/covid19python.git',
    license='GNU General Public License v3 (GPLv3)',
    author='Thomas Woehlke',
    author_email='thomas.woehlke@gmail.com',
    description='Covid19 Data Aggregation - also a Project to learn Python Flask, SQLAlchemy, Celery et al.',
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
        "Natural Language :: German",
        "Natural Language :: English",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Frontends",
        "Framework :: Flask",
    ],
    long_description=readme + history,
    long_description_content_type="text/markdown",
    keywords=keywords,
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    entry_points={},
    extras_require=requires_extras,
    install_requires=requires_dev,
    setup_requires=requires_build,
    tests_require=requires_test,
    scripts=[
        'scripts'+os.sep+'script_setup_requirements.py',
        'scripts'+os.sep+'script_npm_install.py',
        'scripts'+os.sep+'script_get_python_requirements_from_txt.py',
    ],
    python_requires=">= 3.8"
)

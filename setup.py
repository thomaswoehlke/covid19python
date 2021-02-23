import sys

from setuptools import find_packages, setup

version = '0.0.19'

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

readme = open("README.md").read()
history = open("BACKLOG.md").read()

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

requires_setup = [
    "setuptools==53.0.0",
    "wheel==0.36.2",
    "pip-licenses==3.3.0",
    "pip-tools==5.5.0",
    "packaging==20.0",
    "tokenize-rt>=4.1.0",
    "flask-resources==0.6.0",
    "Flask-PluginKit>=3.6.0",
    "Flask-ResponseBuilder>=2.0.12",
    "Flask-Babel>=2",
    "npmdownloader>=1.2.1",
    "pytoml==0.1.21"
]

requires_test = [
    "attrs==20.3.0",
    "blinker==1.4",
    "click==7.1.2",
    "flask==1.1.2",
    "greenlet==1.0.0",
    "itsdangerous==1.1.0",
    "jinja2==2.11.3",
    "markupsafe==1.1.1",
    "more-itertools==8.7.0",
    "packaging==20.9",
    "pluggy==0.13.1",
    "py==1.10.0",
    "pyparsing==2.4.7",
    "pytest-flask==1.1.0",
    "pytest==5.3.2",
    "python-dotenv==0.15.0",
    "test-flask==0.2.0",
    "wcwidth==0.2.5",
    "werkzeug==1.0.1",
    "pytest_celery>=0.0.0a1",
    "pytest-flask-sqlalchemy-1.0.2",
    "pytest-mock-3.5.1"
]

requires_docs = [
    "aiofiles==0.6.0",
    "aiohttp==3.7.3",
    "alabaster==0.7.12",
    "async-timeout==3.0.1",
    "attrs==19.3.0",
    "babel==2.9.0",
    "certifi==2020.12.5",
    "chardet==3.0.4",
    "cleo==0.8.1",
    "click==7.1.2",
    "clikit==0.6.2",
    "crashtest==0.3.1",
    "docutils==0.16",
    "fasteners==0.16",
    "flask-babel==2.0.0",
    "flask-pluginkit==3.6.0",
    "flask-resources==0.6.0",
    "flask-responsebuilder==2.0.13",
    "flask==1.1.2",
    "httplib2==0.19.0",
    "idna==2.10",
    "imagesize==1.2.0",
    "importlib-metadata==1.3.0",
    "itsdangerous==1.1.0",
    "jinja2==2.11.3",
    "json2html==1.3.0",
    "manual-sitemap==19.6.0",
    "markdown==3.3.3",
    "markupsafe==1.1.1",
    "marshmallow==3.10.0",
    "more-itertools==8.0.2",
    "multidict==5.1.0",
    "node-semver==0.8.0",
    "npmdownloader==1.2.1",
    "packaging==20.0",
    "pallets-sphinx-themes==1.2.3",
    "pastel==0.2.1",
    "pbr==5.5.1",
    "pip-licenses==3.3.0",
    "pip-tools==5.5.0",
    "plantuml-creator==1.0.7",
    "plantuml-gentools==0.1.2",
    "plantuml-markdown==3.4.2",
    "plantuml-wrapper==0.1.0",
    "plantuml2freemind==0.8.2",
    "plantuml==0.3.0",
    "pluggy==0.13.1",
    "ptable==0.9.2",
    "py2puml==0.3.1",
    "py==1.8.1",
    "pygments==2.8.0",
    "pylev==1.3.0",
    "pyparsing==2.4.6",
    "pytest==5.3.2",
    "pytz==2021.1",
    "pyyaml==5.4.1",
    "requests==2.25.1",
    "semver==2.13.0",
    "six==1.13.0",
    "snowballstemmer==2.1.0",
    "speaklater==1.3",
    "sphinx-issues==1.2.0",
    "sphinx-tabs==2.0.1",
    "sphinx==3.4.3",
    "sphinxcontrib-applehelp==1.0.2",
    "sphinxcontrib-devhelp==1.0.2",
    "sphinxcontrib-gravizo==0.0.4",
    "sphinxcontrib-htmlhelp==1.0.3",
    "sphinxcontrib-jsmath==1.0.1",
    "sphinxcontrib-log-cabinet==1.0.1",
    "sphinxcontrib-plantuml==0.19",
    "sphinxcontrib-qthelp==1.0.3",
    "sphinxcontrib-serializinghtml==1.1.4",
    "str2bool==1.1",
    "stringcase==1.2.0",
    "tokenize-rt==4.1.0",
    "typing-extensions==3.7.4.3",
    "urllib3==1.26.3",
    "wcwidth==0.1.8",
    "werkzeug==1.0.1",
    "wheel==0.36.2",
    "xmltodict==0.12.0",
    "yarl==1.6.3",
    "zipp==0.6.0"
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

requires_install_minimum = [
    "dash>=1.19.0",
    "dash-extensions>=0.0.45",
    "dtale>=1.34.0",
    "Flask>=1.1.2",
    "Flask-SQLAlchemy>=2.4.4",
    "Flask-Cors>=3.0.10",
    "Flask-BS4==4.5.3.0",
    "SQLAlchemy>=1.3.23",
    "psycopg2>=2.8.6",
    "wget>=3.2",
    "celery[redis]>=5.0.5",
]

requires_install_user_security = [
    "Flask-Multipass>=0.3.3",
    "Flask-Login<0.6.0,>=0.5.0",
]

requires_install_operating = [
    "Flask-Admin>=1.5.7",
    "Flask-Redisboard>=0.2.0",
    "Flask-Monitoring>=1.1.2",
    "flask-healthz>=0.0.2",
    "aiocronjob>=0.2.0",
    "Flask-Caching>=1.9.0"
]

requires_install_nore_flask = [
    "manual-sitemap>=19.6.0",
    "Flask-DB>=0.3.0",
    "flask-pwa>=0.1.0",
    "Flask-Moment>=0.11.0",
    "Flask-CKEditor>=0.4.4.1",
    "flask-checkr>=0.1.2",
    "flask-whooshalchemy3>=0.2.0",
    "flask-was>=0.1.0",
    "Flask-GraphQL>=2.0.1",
    "flask-hintful>=0.0.7",
]

require_install_data_processing = [
    "pyecharts>=1.9.0",
    "pyecharts-extras>=0.0.5",
    "reactive-pyecharts>=1.0.0",
    "visdom>=0.1.8.9",
    "pynndescent>=0.5.1",
    "torch>=1.7.1",
    "numpy>=1.20.1",
    "pandas>=1.1.0",
    "scipy>=1.5.0",
    "StatisticalDiagrams>=20.5",
]

requires_install = [
    "aiocronjob==0.2.6",
    "aiofiles==0.5.0",
    "aiohttp==3.7.3",
    "alabaster==0.7.12",
    "alembic==1.5.4",
    "amqp==5.0.5",
    "appdirs==1.4.4",
    "apscheduler==3.7.0",
    "async-timeout==3.0.1",
    "attrs==19.3.0",
    "babel==2.9.0",
    "billiard==3.6.3.0",
    "blinker==1.4",
    "brotli==1.0.9",
    "celery[redis]==5.0.5",
    "certifi==2020.12.5",
    "cfgv==3.2.0",
    "chardet==3.0.4",
    "cleo==0.8.1",
    "click-didyoumean==0.0.3",
    "click-plugins==1.1.1",
    "click-repl==0.1.6",
    "click==7.1.2",
    "clikit==0.6.2",
    "colorhash==1.0.3",
    "configparser==5.0.1",
    "crashtest==0.3.1",
    "crontab==0.22.9",
    "cycler==0.10.0",
    "dash-bootstrap-components==0.11.3",
    "dash-colorscales==0.0.4",
    "dash-core-components==1.15.0",
    "dash-daq==0.5.0",
    "dash-extensions==0.0.45",
    "dash-html-components==1.1.2",
    "dash-table==4.11.2",
    "dash==1.19.0",
    "dash_renderer==1.9.0",
    "decorator==4.4.2",
    "distlib==0.3.1",
    "docutils==0.16",
    "dominate==2.6.0",
    "dtale==1.34.0",
    "et-xmlfile==1.0.1",
    "fastapi==0.55.1",
    "fasteners==0.16",
    "filelock==3.0.12",
    "flask-admin==1.5.7",
    "flask-babel==2.0.0",
    "flask-bs4==4.5.3.0",
    "flask-caching==1.9.0",
    "flask-checkr==0.1.2",
    "flask-ckeditor==0.4.4.1",
    "flask-compress==1.8.0",
    "flask-cors==3.0.10",
    "flask-db==0.3.0",
    "flask-graphql==2.0.1",
    "flask-healthz==0.0.2",
    "flask-hintful==0.0.7",
    "flask-moment==0.11.0",
    "flask-monitoring==1.1.2",
    "flask-ngrok==0.0.25",
    "flask-pluginkit==3.6.0",
    "flask-pwa==0.1.0",
    "flask-redisboard==0.2.0",
    "flask-resources==0.6.0",
    "flask-responsebuilder==2.0.13",
    "flask-sqlalchemy==2.4.4",
    "flask-was==0.1.0",
    "flask-whooshalchemy3==0.2.0",
    "flask-wtf==0.14.3",
    "flask==1.1.2",
    "future==0.18.2",
    "graphql-core==2.3.2",
    "graphql-server-core==1.2.0",
    "greenlet==1.0.0",
    "h11==0.9.0",
    "httplib2==0.19.0",
    "httptools==0.1.1",
    "identify==1.5.13",
    "idna==2.10",
    "imagesize==1.2.0",
    "importlib-metadata==1.3.0",
    "itsdangerous==1.1.0",
    "jdcal==1.4.1",
    "jinja2==2.11.3",
    "joblib==1.0.1",
    "json2html==1.3.0",
    "jsonpatch==1.28",
    "jsonpointer==2.0",
    "jsonschema==3.2.0",
    "kaleido==0.1.0",
    "kiwisolver==1.3.1",
    "kombu==5.0.2",
    "llvmlite==0.35.0",
    "lz4==3.1.3",
    "mako==1.1.4",
    "manual-sitemap==19.6.0",
    "markdown==3.3.3",
    "markupsafe==1.1.1",
    "marshmallow==3.10.0",
    "matplotlib==3.3.4",
    "more-itertools==8.0.2",
    "multidict==5.1.0",
    "networkx==2.5",
    "node-semver==0.8.0",
    "nodeenv==1.5.0",
    "npmdownloader==1.2.1",
    "numba==0.52.0",
    "numpy==1.20.1",
    "openapi-specgen==0.0.6",
    "openpyxl==3.0.6",
    "packaging==20.0",
    "pallets-sphinx-themes==1.2.3",
    "pandas==1.2.2",
    "pastel==0.2.1",
    "patsy==0.5.1",
    "pbr==3.1.1",
    "pillow==8.1.0",
    "pip-licenses==3.3.0",
    "pip-tools==5.5.0",
    "plantuml-creator==1.0.7",
    "plantuml-gentools==0.1.2",
    "plantuml-markdown==3.4.2",
    "plantuml-wrapper==0.1.0",
    "plantuml2freemind==0.8.2",
    "plantuml==0.3.0",
    "plotly==4.14.3",
    "pluggy==0.13.1",
    "ppscore==1.2.0",
    "pre-commit==2.10.1",
    "prettytable==2.0.0",
    "promise==2.3",
    "prompt-toolkit==3.0.16",
    "psutil==5.8.0",
    "psycopg2==2.8.6",
    "ptable==0.9.2",
    "py2puml==0.3.1",
    "py==1.8.1",
    "pydantic==1.7.3",
    "pyecharts-extras==0.0.5",
    "pyecharts==1.9.0",
    "pygments==2.8.0",
    "pylev==1.3.0",
    "pynndescent==0.5.2",
    "pyparsing==2.4.6",
    "pyrsistent==0.17.3",
    "pytest-flask==1.1.0",
    "pytest==5.3.2",
    "python-dateutil==2.8.1",
    "python-dotenv==0.15.0",
    "python-editor==1.0.4",
    "pytz==2020.5",
    "pyyaml==5.4.1",
    "pyzmq==22.0.3",
    "reactive-pyecharts==1.0.0",
    "redis==3.5.3",
    "requests==2.25.1",
    "retrying==1.3.3",
    "rx==1.6.1",
    "scikit-learn==0.24.1",
    "scipy==1.6.0",
    "semver==2.13.0",
    "simplejson==3.17.2",
    "six==1.13.0",
    "snowballstemmer==2.1.0",
    "speaklater==1.3",
    "sphinx-issues==1.2.0",
    "sphinx-tabs==2.0.1",
    "sphinx==3.4.3",
    "sphinxcontrib-applehelp==1.0.2",
    "sphinxcontrib-devhelp==1.0.2",
    "sphinxcontrib-gravizo==0.0.4",
    "sphinxcontrib-htmlhelp==1.0.3",
    "sphinxcontrib-jsmath==1.0.1",
    "sphinxcontrib-log-cabinet==1.0.1",
    "sphinxcontrib-plantuml==0.19",
    "sphinxcontrib-qthelp==1.0.3",
    "sphinxcontrib-serializinghtml==1.1.4",
    "sqlalchemy-utils==0.36.8",
    "sqlalchemy==1.3.23",
    "squarify==0.4.3",
    "starlette==0.13.2",
    "statisticaldiagrams==20.5",
    "statsmodels==0.12.2",
    "str2bool==1.1",
    "stringcase==1.2.0",
    "strsimpy==0.2.0",
    "test-flask==0.2.0",
    "threadpoolctl==2.1.0",
    "tokenize-rt==4.1.0",
    "toml==0.10.2",
    "torch==1.7.1",
    "torchfile==0.1.0",
    "tornado==6.1",
    "typing-extensions==3.7.4.3",
    "tzlocal==2.1",
    "urllib3==1.26.3",
    "uvicorn==0.11.8",
    "vine==5.0.0",
    "virtualenv==20.4.2",
    "visdom==0.1.8.9",
    "visitor==0.1.3",
    "wcwidth==0.1.8",
    "websocket-client==0.57.0",
    "websockets==8.1",
    "werkzeug==1.0.1",
    "wget==3.2",
    "wheel==0.36.2",
    "whoosh==2.7.4",
    "wtforms==2.3.3",
    "xarray==0.16.2",
    "xlrd==2.0.1",
    "xmltodict==0.12.0",
    "yarl==1.6.3",
    "zipp==0.6.0"
] + pytest_runner

requires_install_groups = [
    requires_install_minimum,
    requires_install_user_security,
    requires_install_operating,
    requires_install_nore_flask,
    require_install_data_processing,
]

for reqs in requires_extras.values():
    requires_extras["all"].extend(reqs)

# for my_group in requires_install_groups:
#    for my_item in my_group:
#        requires_install.append(my_item)

keywords = ""
for kw in keywords_list:
    keywords += " " + kw

packages = find_packages()

setup(
    name='covid19python-thomaswoehlke',
    version=version,
    url='ttps://github.com/thomaswoehlke/covid19python.git',
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
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    keywords=keywords,
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    entry_points={},
    extras_require=requires_extras,
    install_requires=requires_install,
    setup_requires=requires_setup,
    tests_require=requires_test,
    scripts=[
        'scripts/script_setup_requirements',
        'scripts/script_npm_install'
        'scripts/script_get_python_requirements_from_txt'
    ],
    python_requires=">= 3.8"
)

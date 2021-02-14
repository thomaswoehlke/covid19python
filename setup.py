import os

from setuptools import find_packages, setup

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
    "pip-licenses==3.3.0",
    "wheel==0.36.2",
    "tokenize-rt>=4.1.0",
    "flask-resources==0.6.0",
    "Flask-PluginKit>=3.6.0",
    "Flask-ResponseBuilder>=2.0.12",
    "Flask-Babel>=2",
    "npmdownloader>=1.2.1"
]

requires_test = [
    "test-flask>=0.2.0",
    "pytest>=6,<7",
    "pytest-flask>=1.1.0"
]

requires_docs = [
    "sphinx==3.4.3",
    "sphinx-tabs==2.0.1",
    "sphinx-issues==1.2.0",
    "pallets-sphinx-themes==1.2.3",
    "sphinxcontrib-plantuml==0.19",
    "sphinxcontrib-gravizo==0.0.4"
    "py2puml==0.3.1",
    "plantuml-creator == 1.0.7",
    "plantuml-markdown == 3.4.2",
    "plantuml-wrapper == 0.1.0",
    "plantuml2freemind == 0.8.2",
    "plantuml-gentools == 0.1.2",
    "speaklater==1.3"
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

requires_install = {
    "requires_install_minimum": requires_install_minimum,
    "requires_install_user_security": requires_install_user_security,
    "requires_install_operating": requires_install_operating,
    "requires_install_nore_flask": requires_install_nore_flask,
    "require_install_data_processing": require_install_data_processing,
    "all": []
}

for reqs in requires_extras.values():
    requires_extras["all"].extend(reqs)

for reqs in requires_install.values():
    requires_install["all"].extend(reqs)

keywords = ""
for kw in keywords_list:
    keywords += " " + kw

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("flask_resources", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name='thomaswoehlke-covid19python',
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
    python_requires=">= 3.8"
)

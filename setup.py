from setuptools import find_packages, setup

setup(
    name='covid19python-thomaswoehlke',
    version='0.0.14',
    packages=find_packages(),
    url='ttps://github.com/thomaswoehlke/covid19python.git',
    license='GNU General Public License v3.0',
    author='Thomas Woehlke',
    author_email='thomas.woehlke@gmail.com',
    description='Covid19 Data Aggregation - also a Project to learn Python Flask, SQLAlchemy, Celery et al.',
    install_requires=[
        "setuptools>=53.0.0",
        "pip>=21.0.1",
        "wheel>=0.36.2",
        "Flask>=1.1.2",
        "Flask-SQLAlchemy==2.4.4",
        "Flask-Cors==3.0.10",
        "Flask-Login==0.5.0",
        "SQLAlchemy>=1.3.23",
        "psycopg2>=2.8.6",
        "wget>=3.2",
        "celery[redis]>=5.0.5",
        "npmdownloader>=1.2.1",
        "pyecharts>=1.9.0",
        "pyecharts-extras>=0.0.5",
        "tokenize-rt>=4.1.0",
        "numpy>=1.20.0",
        "pandas>=1.2.1",
        "gaphor>=2.2.1",
        "PyGObject>=3.38.0"
    ],
    extras_require={"dotenv": ["python-dotenv"]},
)

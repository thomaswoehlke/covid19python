from setuptools import setup

setup(
    name='covid19python',
    version='0.0.11',
    packages=['org', 'org.woehlke', 'org.woehlke.covid19', 'org.woehlke.covid19.nrw', 'org.woehlke.covid19.rki',
              'org.woehlke.covid19.who', 'org.woehlke.covid19.admin', 'org.woehlke.covid19.europe'],
    url='https://github.com/thomaswoehlke/covid19python',
    license='GNU General Public License v3.0',
    author='thomaswoehlke',
    author_email='thomas.woehlke@gmail.com',
    description='Covid19 Data Aggregation - also a Project to learn Python Flask, SQLAlchemy, Celery et al.'
)

#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='modelapp',
      url='',
      author='',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      version='0.0.1',
      install_requires=[
          'docopt==0.6.2',
          'joblib==0.10.3',
          'toolz==0.8.0',
          'numpy==1.11.0',
          'pandas==0.20.3',
          'scikit-learn==0.18.1',
          'Flask==0.12.2',
          'Flask-Script==2.0.5',
          'Flask-SQLAlchemy==2.2',
          'psycopg2',
          'pytest==3.2.2',
          'flask-jsontools==0.1.1.post0',
          'Flask-API==0.7.1',
          'Flask-Login==0.4.0'
      ],
      include_package_data=True,
      zip_safe=False)

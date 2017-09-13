#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='modelapp',
      url='',
      author='',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      version='0.0.1',
      install_requires=[
          'numpy==1.11.0',
          'scipy==0.19.1',
          'pandas==0.20.3',
          'pytest==3.2.2',
          'docopt==0.6.2',
          'psycopg2==2.7.3.1',
          'scikit-learn==0.19.0',
          'Flask==0.12.2',
          'Flask-Script==2.0.5',
          'Flask-SQLAlchemy==2.2',
          'flask-jsontools==0.1.1.post0',
          'Flask-API==0.7.1',
          'Flask-Login==0.4.0'
      ],
      include_package_data=True,
      zip_safe=False)

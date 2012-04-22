__author__="hkarahan"
__date__ ="$Mar 27, 2010 4:08:12 PM$"

from setuptools import setup,find_packages

setup (
  name = 'p2p.credit',
  version = '0.0.8',
  packages = find_packages(),

  install_requires=[
    'sqlite3>=3.6.19',
    'pysqlite>=2.5.5-r1',
    'memcached>=1.4.1',
    'python-memcached>=1.44',
    'python>=2.6.2-r1',
    'django>=1.1',
    'numpy>=1.3.0-r1',
  ],

  author = 'hasan.karahan81',
  author_email = 'hasan.karahan81@gmail.com',

  url = 'http://blackhan.ch/p2p-credit/',
  license = 'GNU GPL v3.0',
  long_description= 'Web application enabling P2P credit services',

)

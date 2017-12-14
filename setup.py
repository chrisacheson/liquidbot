#!/usr/bin/env python
from setuptools import setup, find_packages
from os.path import dirname, join, isfile
from shutil import copyfile

here = dirname(__file__)

setup(name='bitmex-market-maker',
      version='1.2',
      description='Market making bot for BitMEX API',
      url='https://github.com/BitMEX/sample-market-maker',
      download_url='https://github.com/BitMEX/sample-market-maker/archive/v1.2.zip',
      long_description=open(join(here, 'README.md')).read(),
      author='Samuel Reed',
      author_email='sam@bitmex.com',
      install_requires=[
          'requests',
          'websocket-client',
          'future'
      ]
      )

if not isfile('settings.py'):
  copyfile(join('market_maker', '_settings_base.py'), 'settings.py')
print("\n**** \nImportant!!!\nEdit settings.py before starting the bot.\n****")

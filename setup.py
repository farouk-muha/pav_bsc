# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in pav_bsc/__init__.py
from pav_bsc import __version__ as version

setup(
	name='pav_bsc',
	version=version,
	description='Partner ERPNext - Add Value On Balanced Scorecard',
	author='Farouk Muharram',
	author_email='farouk1dev@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

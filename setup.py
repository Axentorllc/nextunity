# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in nextunity/__init__.py
from nextunity import __version__ as version

setup(
	name='nextunity',
	version=version,
	description='Next Unity',
	author='Dexciss Technology pvt ltd',
	author_email='info@dexciss.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

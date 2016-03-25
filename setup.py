#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages
from opsclient import __author__, __version__, __license__

setup(
	name = 'opsclient',
	version = __version__,
	description = 'Python cliebt library for Nuance OmniPage Server',
	license = __license__,
	author = __author__,
	author_email = 'yoshihiko.aochi@nuance.com',
	url = 'https://github.com/',
	keywords = 'pip github python ops omnipage',
	packages = find_packages()
	install_requires = ["poster", "twisted"]
)

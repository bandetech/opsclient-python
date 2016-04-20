#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages


setup(
	name = 'opsclient',
	version = '0.0.2',
	description = 'Python cliebt library for Nuance OmniPage Server',
	license = 'MIT',
	author = 'Yoshihiko Aochi',
	author_email = 'yoshihiko.aochi@nuance.com',
	url = 'https://github.com/bandetech',
	keywords = 'pip github python ops omnipage',
	packages = find_packages(),
	install_requires = ["poster", "twisted"]
)

#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

from setuptools import dist
dist.Distribution().fetch_build_eggs([
	'Cython>=0.29',
])

import sys
from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools.command.install import install
from Cython.Build import cythonize

import pyximport; pyximport.install()
import about

with open('README.rst') as fin:
	readme = fin.read()

class InstallCommand(install):

	user_options = install.user_options + [
		('no-ws',     None, 'without CKIPWS'),
		('no-parser', None, 'without CKIP-Parser'),
	]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__extensions = []

	def initialize_options(self):
		super().initialize_options()
		self.no_ws     = False
		self.no_parser = False

	def finalize_options(self):
		super().finalize_options()

		if self.no_ws:
			print('Disable CKIPWS support!')
			i = next((i for i, ext_module in enumerate(self.distribution.ext_modules) if ext_module.name == 'ckipws'), None)
			if i is not None: del self.distribution.ext_modules[i]

		if self.no_parser:
			print('Disable CKIP-Parser support!')
			i = next((i for i, ext_module in enumerate(self.distribution.ext_modules) if ext_module.name == 'ckipparser'), None)
			if i is not None: del self.distribution.ext_modules[i]

setup(
	name=about.__title__,
	version=about.__version__,
	author=about.__author_name__,
	author_email=about.__author_email__,
	maintainer=about.__author_name__,
	maintainer_email=about.__author_email__,
	description=about.__description__,
	long_description=readme,
	long_description_content_type='text/x-rst',
	url=about.__url__,
	download_url=about.__download_url__,
	platforms=['linux_x86_64'],
	license=about.__license__,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Cython',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX :: Linux',
		'Natural Language :: Chinese (Traditional)',
	],
	ext_modules=cythonize(
		[
			Extension('ckipws',
				sources=['ckipws/ckipws.pyx'],
				libraries=['WordSeg'],
			),
			Extension('ckipparser',
				sources=['ckipparser/ckipparser.pyx'],
				libraries=['CKIPCoreNLP', 'CKIPParser', 'CKIPSRL', 'CKIPWS'],
			),
		],
		build_dir='build',
	),
	cmdclass={
		'install': InstallCommand,
	},
)

#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function

__author__    = 'Mu Yang <emfomy@gmail.com>'
__copyright__ = 'Copyright 2018-2019'

from setuptools import dist
dist.Distribution().fetch_build_eggs([
	'Cython>=0.29',
])

import os
import sys

from setuptools import setup
from setuptools.extension import Extension
from setuptools.command.install import install
from setuptools.command.develop import develop
from Cython.Build import cythonize

import pyximport; pyximport.install()
import about

with open('README.rst') as fin:
	readme = fin.read()

def os_environ_append(name, dirpath):
	if name in os.environ:
		os.environ[name] += os.pathsep + dirpath
	else:
		os.environ[name] = dirpath

def os_environ_prepend(name, dirpath):
	if name in os.environ:
		os.environ[name] = dirpath + os.pathsep + os.environ[name]
	else:
		os.environ[name] = dirpath


class CommandMixin(object):

	user_options = [
		('ws',        None, 'with CKIPWS [default]'),
		('parser',    None, 'with CKIP-Parser [default]'),
		('no-ws',     None, 'without CKIPWS'),
		('no-parser', None, 'without CKIP-Parser'),

		('ws-dir=',       None, 'CKIPWS root directory'),
		('ws-lib-dir=',   None, 'CKIPWS libraries directory [default is <ws-dir>/lib]'),
		('ws-share-dir=', None, 'CKIPWS share directory [default is <ws-dir>]'),

		('parser-dir=',       None, 'CKIP-Parser root directory'),
		('parser-lib-dir=',   None, 'CKIP-Parser libraries directory [default is "<parser-dir>/lib"]'),
		('parser-share-dir=', None, 'CKIPWS share directory [default is "<parser-dir>"]'),

		('data2-dir=', None, 'CKIPWS "Data2" directory [default is "<ws-share-dir>/Data2" or "<parser-share-dir>/Data2"]'),
		('rule-dir=',  None, 'CKIP-Parser "Rule" directory [default is "<parser-share-dir>/Rule"]'),
		('rdb-dir=',   None, 'CKIP-Parser "RDB" directory [default is "<parser-share-dir>/RDB"]'),
	]

	negative_opt = {
		'no-ws':     'ws',
		'no-parser': 'parser',
	}

	def initialize_options(self):
		self.ws     = True
		self.parser = True

		self.ws_dir     = None

		self.ws_lib_dir   = None
		self.ws_share_dir = None

		self.parser_dir = None
		self.parser_lib_dir   = None
		self.parser_share_dir = None

		self.data2_dir = None
		self.rule_dir  = None
		self.rdb_dir   = None

		super(CommandMixin, self).initialize_options()

	def finalize_options(self):

		# subdirectory
		opt_subdirectory = [
			('ws_lib_dir',      'ws_dir',     'lib',),
			('ws_share_dir',    'ws_dir',     '',),
			('parser_lib_dir',  'parser_dir', 'lib',),
			('parser_share_dir','parser_dir', '',),

			('data2_dir', 'ws_share_dir',     'Data2',),
			('data2_dir', 'parser_share_dir', 'Data2',),
			('rule_dir',  'parser_share_dir', 'Rule',),
			('rdb_dir',   'parser_share_dir', 'RDB',),
		]
		for opt0, opt1, subdir in opt_subdirectory:
			dir0 = getattr(self, opt0)
			dir1 = getattr(self, opt1)
			if not dir0 and dir1:
				setattr(self, opt0, os.path.join(dir1, subdir))

		# directory
		opt_directory = [
			'ws_lib_dir',
			'parser_lib_dir',
			'data2_dir',
			'rule_dir',
			'rdb_dir',
		]
		for opt0 in opt_directory:
			dir0 = getattr(self, opt0)
			if dir0 and not os.path.isdir(dir0):
				raise IOError('--%s (%s) is not a directory' % (opt0.replace('_', '-'), dir0,))

		super(CommandMixin, self).finalize_options()

	def run(self):

		# CKIPWS
		if self.ws:
			print('- Enable CKIPWS support')
			if self.ws_lib_dir:
				print('- Use CKIPWS library from (%s)' % self.ws_lib_dir)
				i = next((i for i, em in enumerate(self.distribution.ext_modules) if em.name == 'ckipws'), None)
				self.distribution.ext_modules[i].library_dirs.append(self.ws_lib_dir)
				self.distribution.ext_modules[i].runtime_library_dirs.append(self.ws_lib_dir)
		else:
			print('- Disable CKIPWS support')
			i = next((i for i, em in enumerate(self.distribution.ext_modules) if em.name == 'ckipws'), None)
			if i is not None: del self.distribution.ext_modules[i]

		# CKIP-Parser
		if self.parser:
			print('- Enable CKIP-Parser support')
			if self.parser_lib_dir:
				print('- Use CKIP-Parser library from (%s)' % self.parser_lib_dir)
				i = next((i for i, em in enumerate(self.distribution.ext_modules) if em.name == 'ckipparser'), None)
				self.distribution.ext_modules[i].library_dirs.append(self.parser_lib_dir)
				self.distribution.ext_modules[i].runtime_library_dirs.append(self.parser_lib_dir)
		else:
			print('- Disable CKIP-Parser support')
			i = next((i for i, em in enumerate(self.distribution.ext_modules) if em.name == 'ckipparser'), None)
			if i is not None: del self.distribution.ext_modules[i]


		# Data
		if self.data2_dir:
			print('- Use "Data2" from (%s)' % self.data2_dir)
			self.data_files('share/pyckip/Data2/', self.data2_dir)

		if self.rule_dir:
			print('- Use "Rule" from (%s)' % self.rule_dir)
			self.data_files('share/pyckip/Rule/', self.rule_dir)

		if self.rdb_dir:
			print('- Use "RDB" from (%s)' % self.rdb_dir)
			self.data_files('share/pyckip/RDB/', self.rdb_dir)

		super(CommandMixin, self).run()

	def data_files(self, prefix, dirtop):
		for dirpath, _, files in os.walk(dirtop):
			self.distribution.data_files.append((
				os.path.join(prefix, os.path.relpath(dirpath, dirtop)),
				[os.path.join(dirpath, file) for file in files],
			))

class InstallCommand(CommandMixin, install):
	user_options = install.user_options + CommandMixin.user_options
	negative_opt = install.negative_opt
	negative_opt.update(CommandMixin.negative_opt)

	def __init__(self, *args, **kwargs):
		install.__init__(self, *args, **kwargs)

class DevelopCommand(CommandMixin, develop):
	user_options = develop.user_options + CommandMixin.user_options
	negative_opt = develop.negative_opt
	negative_opt.update(CommandMixin.negative_opt)

	def __init__(self, *args, **kwargs):
		develop.__init__(self, *args, **kwargs)

setup(
	name=about.__title__,
	version=about.__version__,
	author=about.__author_name__,
	author_email=about.__author_email__,
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
				libraries=['CKIPCoreNLP'],
			),
		],
		build_dir='build',
	),
	data_files=[],
	cmdclass={
		'install': InstallCommand,
		'develop': DevelopCommand,
	},
)

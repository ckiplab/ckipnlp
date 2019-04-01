#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import dist
dist.Distribution().fetch_build_eggs([
	'Cython>=0.29',
])

from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

with open('ckipws/ckipws.pyx') as fin:
	for line in fin:
		if '__version__' in line:
			exec(line)
			break

with open('README.rst') as fin:
	description = fin.read()

setup(
	name='pyckip',
	version=__version__,
	packages=['ckipws'],
	author='Mu Yang',
	author_email='emfomy@gmail.com',
	description='CKIP NLP Wrappers',
	long_description=description,
	long_description_content_type='text/x-rst',
	url='https://github.com/emfomy/pyckip',
	download_url='https://github.com/emfomy/pyckip/tarball/'+__version__,
	classifiers=[
		'Development Status :: 3 - Alpha',
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
	include_package_data=True,
)

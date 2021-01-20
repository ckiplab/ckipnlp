#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'Mu Yang <http://muyang.pro>'
__copyright__ = '2018-2020 CKIP Lab'
__license__ = 'GPL-3.0'

from setuptools import setup, find_namespace_packages
import ckipnlp as about

################################################################################

def main():

    with open('README.rst', encoding='utf-8') as fin:
        readme = fin.read()

    setup(
        name='ckipnlp',
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
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3 :: Only',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: POSIX :: Linux',
            'Natural Language :: Chinese (Traditional)',
        ],
        python_requires='>=3.6',
        packages=find_namespace_packages(include=['ckipnlp', 'ckipnlp.*',]),
        install_requires=[
            'appdirs>=1.4.3',
            'numpy>=1.18',
            'treelib>=1.5.5',
        ],
        extras_require={
            'classic': ['ckip-classic>=1.1.2'],
            'tagger': ['ckiptagger[tf]>=0.2.1'],
            'tagger-gpu': ['ckiptagger[tfgpu]>=0.2.1'],
        },
        data_files=[],
    )

################################################################################

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
long_description = readme
doclink = '''
Documentation
-------------

The full documentation is at http://workbench.rtfd.org. '''
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='workbench',
    version='0.1.0',
    description='A medium-data framework for security research and development teams.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Brian Wylie',
    author_email='briford@supercowpowers.com',
    url='https://github.com/brifordwylie/workbench',
    packages=['workbench'],
    package_dir={'workbench': 'workbench'},
    scripts = ['workbench'],
    include_package_data=True,
    tests_require=['pytest'],
    install_requires=[],
    license='MIT',
    zip_safe=False,
    keywords='workbench, security, python',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    extras_require={
        'testing': ['pytest'],
    }    
)

#!/usr/bin/env python

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_version(filename):
    """Extract __version__ from file by parsing it."""
    with open(filename) as fp:
        for line in fp:
            if line.startswith('__version__'):
                exec(line)
                return __version__

setup(
    name='radiopy',
    version=get_version('radio.py'),
    description='An interface for mplayer aimed at listening to streaming radio.',
    url='http://www.guyrutenberg.com/radiopy',
    author='Guy Rutenberg',
    author_email='guyrutenberg@gmail.com',
    license = 'GPLv2+',
    packages=['radiopy'],
    scripts=['radio.py'],
    long_description=read('README.rst'),
    package_data={'radiopy': ['data/radiopy.default']},
    install_requires = ['beautifulsoup4'],

    classifiers = [
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        ],
)


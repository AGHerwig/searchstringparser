#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from __future__ import (absolute_import, print_function)

import io
import os.path as osp
import re
from glob import glob

from setuptools import (find_packages, setup)


def read(*names, **kwargs):
    return io.open(
        osp.join(osp.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='searchstringparser',
    version='0.2.3',
    license='BSD',
    description='Parse a more general search syntax to conform with a particular SQL dialect.',
    long_description='%s\n%s' % (read('README.rst'), re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    author='Moritz Emanuel Beber',
    author_email='beber@molgen.mpg.de',
    url='https://github.com/AGHerwig/searchstringparser',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[osp.splitext(osp.basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Database :: Front-Ends',
    ],
    keywords=[
        'SQL',
        'PostgreSQL',
        'search',
        'parser'
    ],
    install_requires=[
        'ply'
    ],
)

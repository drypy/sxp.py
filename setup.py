#!/usr/bin/env python

from distutils.core import setup

setup(name='sxp',
      version='0.0.1',
      author='Arto Bendiken',
      author_email='arto.bendiken@gmail.com',
      maintainer='Arto Bendiken',
      maintainer_email='arto.bendiken@gmail.com',
      url='http://python.org/pypi/sxp',
      description='SXP for Python',
      license='MIT',
      long_description='A standardized S-expression format for data interchange, based on a subset of the IEEE Scheme and DSSSL standards.',
      download_url='',
      classifiers=[
        'Keywords: sxp s-expr s-expression scheme lisp',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
      packages=['sxp'],
      package_dir = {'': 'lib'})

#!/usr/bin/env python

import imp

from setuptools import setup, find_packages

version = imp.load_source('aupyom.version', 'aupyom/version.py')


setup(name='aupyom',
      version=version.version,
      packages=find_packages(),

      install_requires=[
            'numpy',
            'librosa',
            'sounddevice',
      ],

      extras_require={
          'doc': ['sphinx', ],
      },

      setup_requires=['setuptools_git >= 0.3', ],

      exclude_package_data={'': ['README', '.gitignore']},
      package_data={'': ['example_data/*']}

      author='Pierre Rouanet',
      author_email='pierre.rouanet@gmail.com',
      description='Real-time Audio time-scale and pitch modification.',
      url='https://github.com/pierre-rouanet/aupyom',
      license='GNU GENERAL PUBLIC LICENSE Version 3',

      classifiers=[
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 3",
          "Topic :: Scientific/Engineering", ],

      **extra
      )

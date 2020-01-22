#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
  name='keep-cli',
  version='1.0.0',
  license='MIT',
  description='keep is a command line client for Google Keep',
  author='Adam Miller',
  author_email='miller@adammiller.io',
  url='https://github.com/adammillerio/keep',
  download_url='https://github.com/adammillerio/keep/archive/v1.0.0.tar.gz',
  keywords=['google', 'keep', 'notes'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3 :: Only',
  ],
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
    'click>=7.0',
    'gkeepapi>=0.11.9'
  ],
  entry_points='''
    [console_scripts]
    keep=keep.cli:cli
  '''
)

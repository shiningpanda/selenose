#-*- coding: utf-8 -*-
try: import setuptools
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    
from setuptools import setup, find_packages

setup(
    name = 'rdflib',
    version = '3.1.0',
    packages = find_packages(),
)

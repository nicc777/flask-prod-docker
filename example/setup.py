# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='flask-app',
    version='0.0.1',
    description='flask-app',
    long_description='flask-app',
    author='Nico Coetzee',
    author_email='nicc77@gmail.com',
    url='http://google.com/',
    license='BSD',
    packages=find_packages(exclude=('tests', 'docs')), 
    install_requires=['flask'],
    include_package_data=True, 
)

# EOF

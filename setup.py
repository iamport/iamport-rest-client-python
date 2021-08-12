# -*- coding: utf-8 -*-

import io
import os

from setuptools import setup, find_packages


def get_spec(filename):
    def wrapper():
        here = os.path.dirname(__file__)
        result = {}
        with io.open(os.path.join(here, filename), encoding='utf-8') as src_file:
            result = src_file.read()
        return result
    return wrapper


get_readme = get_spec('README.rst')
get_requirements = get_spec('requirements.txt')
setup(
    name='iamport-rest-client',
    version='0.8.2',
    description="REST client for I'mport;(http://www.iamport.kr)",
    long_description=get_readme(),
    url='https://github.com/iamport/iamport-rest-client-python',
    packages=find_packages(),
    author='PerhapsSPY',
    author_email='perhapsspy@gmail.com',
    include_package_data=True,
    install_requires=get_requirements(),
    license='MIT',
    zip_safe=False,
    data_files=[
        (
            'shared/typehints/python2.7',
            ['iamport/client.pyi'],
        ),
        (
            'shared/typehints/python3.6',
            ['iamport/client.pyi'],
        ),
        (
            'shared/typehints/python3.7',
            ['iamport/client.pyi'],
        ),
        (
            'shared/typehints/python3.8',
            ['iamport/client.pyi'],
        ),
        (
            'shared/typehints/python3.9',
            ['iamport/client.pyi'],
        ),
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)

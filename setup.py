# -*- coding: utf-8 -*-

import pathlib

from setuptools import setup


def read(file_name):
    file_path = pathlib.Path(__file__).parent / file_name
    return file_path.read_text('utf-8')


setup(
    name='cibopath',
    version='0.1.0',
    author='Raphael Pierzina',
    author_email='raphael@hackebrot.de',
    maintainer='Raphael Pierzina',
    maintainer_email='raphael@hackebrot.de',
    license='BSD',
    url='https://github.com/hackebrot/cibopath',
    description='Search Cookiecutters on GitHub.',
    long_description=read('README.rst'),
    packages=[
        'cibopath',
    ],
    package_dir={'cibopath': 'cibopath'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click',
        'aiohttp',
    ],
    entry_points={
        'console_scripts': [
            'cibopath = cibopath.cli:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords=['cookiecutter', 'web scraping', 'asyncio', 'command-line'],
)

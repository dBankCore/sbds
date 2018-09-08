# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='dpds',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'dpds=dpds.cli:dpds',
            'populate=dpds.storages.db.scripts.populate:populate',
        ],
    },
)

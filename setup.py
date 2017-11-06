#!/usr/bin/env python
""" Setup to allow pip installs of pok-eco module """

from setuptools import setup

setup(
    name='asict_cert',
    version='0.0.3',
    description='ASICT CERT Integrations ',
    author='METID - Politecnico di Milano',
    url='http://www.metid.polimi.it',
    license='AGPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages=['asictapi'],
    dependency_links=[],
    install_requires=[
        "django==1.8.7",
        "django-celery==3.1.16",
        "tincan==0.0.5",
        "pyoai==2.4.4"
    ]
)

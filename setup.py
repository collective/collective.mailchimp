# -*- coding: utf-8 -*-
"""Installer for the collective.mailchimp package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open('README.rst').read()
    + '\n'
    + 'Contributors\n'
    + '============\n'
    + '\n'
    + open('CONTRIBUTORS.rst').read()
    + '\n'
    + open('CHANGES.rst').read()
    + '\n'
)


setup(
    name='collective.mailchimp',
    version='4.0.0a6.dev0',
    description="MailChimp integration for Plone.",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Plone",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone MailChimp Mail Newsletter',
    author='kitconcept GmbH (Timo Stollenwerk)',
    author_email='stollenwerk@kitconcept.com',
    url='https://pypi.org/project/collective.mailchimp/',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['collective'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        'setuptools',
        'Products.CMFPlone',
        'plone.app.portlets',
        'plone.app.registry',
        'plone.app.upgrade',
        'requests',
    ],
    extras_require={'test': ['mock', 'plone.app.testing', 'plone.api']},
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)

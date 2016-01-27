from setuptools import setup, find_packages

version = '1.4.2.dev0'
description = 'MailChimp integration for Plone.'
long_description = \
    open("README.rst").read() + "\n" + \
    open("CHANGES.rst").read()

setup(name='collective.mailchimp',
      version=version,
      description=description,
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
      ],
      keywords='',
      author='Timo Stollenwerk',
      author_email='stollenwerk@kitconcept.com',
      url='http://github.com/collective/collective.mailchimp',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.app.portlets',
          'plone.app.registry',
          'requests',
      ],
      extras_require={
          'test': [
              'mock',  # new, backport from Python 3.3
              'plone.app.testing',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )

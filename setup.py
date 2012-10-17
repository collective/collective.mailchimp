from setuptools import setup, find_packages

version = '1.0'
description = 'MailChimp integration for Plone.'
long_description = \
    open("README.rst").read() + "\n" + \
    open("CHANGES.txt").read()

setup(name='collective.mailchimp',
      version=version,
      description=description,
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
      ],
      keywords='',
      author='Timo Stollenwerk',
      author_email='contact@timostollenwerk.net',
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
          'postmonkey',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'mocker',
              'plone.mocktestcase',
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

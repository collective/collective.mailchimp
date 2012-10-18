Introduction
============

.. image:: https://secure.travis-ci.org/collective/collective.mailchimp.png

MailChimp integration for Plone.

MailChimp_ helps you design email newsletters, share
them on social networks, integrate with services you already use, and track
your results.

collective.mailchimp has been written from the scratch in order to replace
raptus.mailchimp_ for newer
versions of Plone (> 4.0).

.. _MailChimp: http://mailchimp.com
.. _raptus.mailchimp: http://plone.org/products/raptus.mailchimp

The difference between collective.mailchimp and raptus.mailchimp is:

- postmonkey_ instead of greatape_ as Python wrapper
- z3c.form_ instead of formlib for forms
- plone.app.registry_ instead of portal_properties for storing properties
- it is tested by automated software tests

.. _postmonkey: http://pypi.python.org/pypi/postmonkey
.. _greatape: http://pypi.python.org/pypi/greatape
.. _z3c.form: http://pypi.python.org/pypi/z3c.form
.. _plone.app.registry: http://pypi.python.org/pypi/plone.app.registry

collective.mailchimp is tested on Plone 4.x and should work on Plone > 3.3
(with the appropriate version pins).


Installation
============

Just add collective.mailchimp to the eggs section of your buildout.


Issue Tracker
=============

Please report bugs to the `issue tracker on github`_.

.. _`issue tracker on github`: https://github.com/collective/collective.mailchimp/issues

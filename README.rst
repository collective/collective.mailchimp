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

The difference between raptus.mailchimp and collective.mailchimp is:

    - c.mailchimp uses PostMonkey instead of greatape as Python wrapper
    - c.mailchimp uses z3c.form instead of formlib for forms
    - c.mailchimp uses plone.app.registry instead of portal_properties
      for storing properties.

collective.mailchimp is tested on Plone 4.x and should work on Plone > 3.3
(with the appropriate version pins).


Installation
============

Just add collective.mailchimp to the eggs section of your buildout.

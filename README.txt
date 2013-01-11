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


Multiple MailChimp Lists
========================

collective.mailchimp supports multiple MailChimp lists. The MailChimp portlet
allows administators to choose a MailChimp list from a dropdown list for each
portlet. The MailChimp newsletter view (@@newsletter) allows to provide a
list_id (see your MailChimp account) as optional URL parameter::

  http://localhost:8080/Plone/@@newsletter?list_id=f3247645gs

If no URL parameter is provided the form just chooses the first MailChimp list
available (which is fine as long as you have just one list anyway).


Extend Newsletter Subscription Form
===================================

The collective.mailchimp newsletter form (used in the separate view as well
as in the portlet) can be extended without touching the code of
collective.mailchimp. See
https://github.com/collective/collective.mailchimp/blob/master/collective/mailchimp/browser/extender.py and
https://github.com/collective/collective.mailchimp/blob/master/collective/mailchimp/browser/extender.zcml for details.
In general this works the same way as for plone.app.discussion: http://packages.python.org/plone.app.discussion/howtos/howto_extend_the_comment_form.html.


Issue Tracker
=============

Please report bugs to the `issue tracker on github`_.

.. _`issue tracker on github`: https://github.com/collective/collective.mailchimp/issues

.. image:: https://secure.travis-ci.org/collective/collective.mailchimp.png
    :target: http://travis-ci.org/collective/collective.mailchimp

.. image:: https://img.shields.io/coveralls/collective/collective.mailchimp/master.svg
    :target: https://coveralls.io/r/collective/collective.mailchimp

.. image:: https://landscape.io/github/collective/collective.mailchimp/master/landscape.svg
   :target: https://landscape.io/github/collective/collective.mailchimp/master
   :alt: Code Health

.. image:: https://img.shields.io/pypi/status/collective.mailchimp.svg
    :target: https://pypi.python.org/pypi/collective.mailchimp/
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/v/collective.mailchimp.svg
    :target: https://pypi.python.org/pypi/collective.mailchimp/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/collective.mailchimp.svg
    :target: https://pypi.python.org/pypi/collective.mailchimp/
    :alt: License

.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

Introduction
============

.. image:: https://raw.githubusercontent.com/collective/collective.mailchimp/master/kitconcept.png
   :alt: kitconcept
   :target: https://kitconcept.com/

MailChimp integration for Plone 4 and 5.

MailChimp helps you design email newsletters, share them on social networks, integrate with services you already use, and track your results.

collective.mailchimp provides a @newsletter view to let visitors subscribe to one or more MailChimp mailing lists. It also provides a MailChimp portlet in case you want to display your newsletter subscription as part of an existing site.

The newsletter subscriptions forms in both the view and the portlet are extendable, so you can add custom fields that can be stored in your MailChimp subscriber list.

It also comes with a MailChimp control panel to let you enter your MailChimp credentials for your Plone site.

collective.mailchimp is tested on Plone 4.x and 5.x and should work on Plone > 3.3
(with the appropriate version pins for plone.app.registry and z3c.form).


Installation
============

Install collective.mailchimp by adding it to your buildout::

  [buildout]

  ...

  eggs =
      collective.mailchimp

and then running "bin/buildout".


Multiple MailChimp Lists
========================

collective.mailchimp supports multiple MailChimp lists. The MailChimp portlet
allows administators to choose a MailChimp list from a dropdown list for each
portlet. The MailChimp newsletter view (@@newsletter) allows to provide a
list_id (see your MailChimp account) as optional URL parameter::

  http://localhost:8080/Plone/@@newsletter?list_id=f3247645gs

If no URL parameter is provided the form just chooses the first MailChimp list
available (which is fine as long as you have just one list anyway).


Preselect Interest Groups
=========================

collective.mailchimp supports MailChimp's interest groups. In case there is more than one single group you might want to pre-select some of the groups. To
do so add one or more 'preselect_group' parameters to the URL that points to
your MailChimp newsletter form. For instance to select the first and the fifth
group entry use the following link::

    http://localhost:8080/Plone/@@newsletter?preselect_group=0&preselect_group=4

Note: if you used version 1.4.1 of collective.mailchimp or earlier,
you may no longer see the interest groups on the subscribe form.  You
should visit the control panel again.  This will update the data
automatically.


Extend Newsletter Subscription Form
===================================

The collective.mailchimp newsletter form (used in the separate view as well
as in the portlet) can be extended without touching the code of
collective.mailchimp.

.. note::

  - https://github.com/collective/collective.mailchimp/blob/master/src/collective/mailchimp/browser/extender.py

  - https://github.com/collective/collective.mailchimp/blob/master/src/collective/mailchimp/browser/extender.zcml

  - http://packages.python.org/plone.app.discussion/howtos/howto_extend_the_comment_form.html.


History
=======

collective.mailchimp has been written from the scratch in order to replace
raptus.mailchimp_ for newer versions of Plone (> 4.0).

.. _MailChimp: http://mailchimp.com
.. _raptus.mailchimp: http://plone.org/products/raptus.mailchimp

The difference between collective.mailchimp and raptus.mailchimp is:

- Directly use the MailChimp API instead of greatape_ as Python wrapper (because greatape is completely untested, does not support the latest MailChimp API version and seems to be not actively developed any longer)
- z3c.form_ instead of formlib for forms (because formlib is deprecated)
- plone.app.registry_ instead of portal_properties for storing properties (because portal_properties will be deprecated soon)
- it is tested by automated software tests (because untested code is broken code)

.. _greatape: http://pypi.python.org/pypi/greatape
.. _z3c.form: http://pypi.python.org/pypi/z3c.form
.. _plone.app.registry: http://pypi.python.org/pypi/plone.app.registry


Issue Tracker
=============

Please report bugs to the `issue tracker on github`_.


Credits
=======

.. image:: https://raw.githubusercontent.com/collective/collective.mailchimp/master/kitconcept.png
   :height: 461px
   :width: 100px
   :scale: 100 %
   :alt: kitconcept
   :align: center
   :target: https://www.kitconcept.com/

This plugin is developed and maintained by `kitconcept`_.

If you are having issues, please let us know.


License
=======

The project is licensed under the GPLv2.

.. _`issue tracker on github`: https://github.com/collective/collective.mailchimp/issues

.. _`kitconcept`: https://kitconcept.com


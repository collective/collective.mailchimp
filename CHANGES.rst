Changelog
=========

3.1.0 (2020-01-13)
------------------

New Features:

- Add Plone 5.2 and Python 3.7 classifiers.
  [timo]

- Add uninstall profile
  [erral]

Bug Fixes:

- Don't show interest groups if empty
  [laulaz]

- Fix existing French translations
  [laulaz]

- Redirect to navigation root after (un)subscription
  [daggelpop]


3.0.0 (2019-06-14)
------------------

New Features:

- Prepare to work with Python 3.
  Isort, black, fixed deprecated Python 2 syntax AST errors.
  implements to implementer.
  Fix imports with six and avoid circular imports.
  [jensens]


2.2.2 (2018-06-07)
------------------

Bugfixes:

- Fix error handling in @@newsletter to validate form extenders
  [csenger]


2.2.1 (2018-01-05)
------------------

Bugfixes:

- Plone 5.1 compatibility.
  [timo]


2.2.0 (2017-12-07)
------------------

New Features:

- Make plone.app.imaging a test dependency only in setup.py. This fixes an
  issue with Plone 5.1 and plone.restapi. plone.app.imaging is a hard
  dependency on Plone 5.0 (CMFPlone) and optional on Plone 5.1.
  [timo]


2.1.0 (2017-09-12)
------------------

New Features:

- Plone 5.0.8 compatibility. Add plone.app.imaging to dependencies in setup.py.
  [timo]

- Add @@unsubscribe-newsletter.
  [csenger]

- Added basic Romanian translation
  [ichim-david]

Bugfixes:

- Updated Dutch translations.
  [jladage]

- Fixed ignoral of new locales directory because of option set in gitignore
  [ichim-david]


2.0.2 (2016-02-02)
------------------

Bugfixes:

- Fixed MANIFEST.in so all files are added.  Releases 2.0 and 2.0.1
  were missing non Python files.  [maurits]


2.0.1 (2016-01-29)
------------------

Bugfixes:

- Add upgrade step to reload new src folder. Make sure you run the upgrade step, otherwise the add-on will not work properly. This fixes https://github.com/collective/collective.mailchimp/issues/21.
  [timo]


2.0 (2016-01-28)
----------------

- Move code to src folder to follow best practice.
  [timo]

- Set default value for interests to '{}' instead of None. This fixes https://github.com/collective/collective.mailchimp/issues/19.
  [timo]

- Added support for Plone 5, kept 4.3 compatibility.
  [jladage, didrix, maurits]

- Updated to version 3.0 of the mailchimp api.  The data that we get
  from mailchimp with this api version is changed.  When you have
  interest groups in your lists, and you do not see them anymore on
  the subscribe form, you should visit the control panel again.  This
  will update the data automatically.
  [jladage, didrix, maurits]

- Remove bare excepts.
  [timo]


1.4.1 (2015-05-04)
------------------

- Try to avoid some needless registry updates.
  [maurits]

- Disable inline validation in the mailchimp control panel.  It may
  change the cache based on a new api key that the user has not yet
  saved.
  [maurits]

- Remove mailchimp object before updating cache.  Otherwise a change
  in the api key is not picked up until after a restart.
  [maurits]


1.4.0 (2015-04-29)
------------------

- Fix invalid pypi classifier.
  [timo]

- Show control panel even when api key is invalid.
  Fixes issue #8.
  [maurits]

- Fix fallback for missing cache after startup.
  [pbauer]

- Add italian translation.
  [gborelli]

- Fix UnicodeEncodeError
  [pbauer]

- Add persistent cache in the registry for the connection.
  [toutpt]

- Add french translations
  [toutpt]

- Add brazilian translation.
  [cleberjsantos]


1.3.1 (2013-03-03)
------------------

- Fix broken group subscription which has been introduced in 1.3.0.
  [timo]


1.3.0 (2013-03-03)
------------------

- Add option to preselect interest groups in the newsletter form.
  [timo]


1.2.1 (2013-02-13)
------------------

- Fix 1.2.0 upgrade step.
  [timo]


1.2.0 (2013-02-13)
------------------

- Make newsletter view not fail if no default_list has been selected.
  [timo]

- German translation updated.
  [timo]

- Styles for newsletter subscription form added.
  [timo]


1.1.1 (2013-02-01)
------------------

- Fix mailchimp control panel which fails if no valid MailChimp API key has
  been provided.
  [timo]


1.1.0 (2013-01-23)
------------------

- Dutch translation added.
  [sjoerdve]

- Make NewsletterForm extendable.
  [timo]

- Use MailChimp list settings from the control panel. Note: You have to
  reinstall collective.mailchimp, otherwise you will end up with a
  "KeyError: 'Interface .. defines a field .., for which there is no record.'"
  [timo]

- Support for MailChimp interest groups added. For now this feature only works
  with one single list.
  [timo]

- Email type option added.
  [timo]

- Rename AvailableListsVocabulary to AvailableLists.
  [timo]

- Add fieldsets to MailChimp control panel.
  [timo]

- Add a MailchimpLocator utility to encapsulate all MailChimp API calls.
  [timo]

- Allow multiple lists for newsletter view; add mailchimp locator to
  encapsulate api calls.
  [timo]

- Add new default_list setting to allow administrators to choose their default
  MailChimp list for the @@newsletter view.
  [timo]

- Add email_type_is_optional setting to allow administrators to choose if they
  want to allow users to choose their own email_type.
  [timo]

- Make README and CHANGES .rst files.
  [timo]


1.0.3 (2012-12-05)
------------------

- Missing .mo files added.
  [timo]


1.0.2 (2012-12-05)
------------------

- Raise a more specific error when an email has been already subscribed to a
  newsletter.
  [timo]

- German translations updated.
  [timo]


1.0.1 (2012-10-28)
------------------

- Fix MANIFEST.in to include readme and changelog.
  [jone]


1.0 (2012-10-17)
----------------

- Initial release
  [timo]

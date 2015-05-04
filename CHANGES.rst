Changelog
=========

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

Fix MANIFEST.in to include readme and changelog.
[jone]


1.0 (2012-10-17)
----------------

- Initial release
  [timo]

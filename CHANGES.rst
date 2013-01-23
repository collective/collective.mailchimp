Changelog
=========

1.1.0 (2013-01-23)
------------------

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

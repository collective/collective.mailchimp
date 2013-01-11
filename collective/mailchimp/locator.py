from postmonkey import PostMonkey
from collective.mailchimp.interfaces import IMailchimpSettings
from zope.component import getUtility
from postmonkey import MailChimpException
from plone.registry.interfaces import IRegistry
from zope.interface import implements
from collective.mailchimp.interfaces import IMailchimpLocator


class MailchimpLocator(object):
    """Utility for MailChimp API calls.
    """

    implements(IMailchimpLocator)

    def connect(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IMailchimpSettings)
        self.mailchimp = PostMonkey(self.settings.api_key)

    def lists(self):
        """Return all available MailChimp lists.
        http://apidocs.mailchimp.com/api/rtfm/lists.func.php
        """
        #print("MAILCHIMP LOCATOR: lists")
        self.connect()
        try:
            # lists returns a dict with 'total' and 'data'. we just need data
            return self.mailchimp.lists()['data']
        except MailChimpException:
            pass

    def groups(self, id):
        """Return all available MailChimp interest groups.

        @id: the list id to connect to. e.g. u'a1346945ab'. Not the web_id!

        http://apidocs.mailchimp.com/api/rtfm/listinterestgroupings.func.php
        """
        #print("MAILCHIMP LOCATOR: groups")
        self.connect()
        try:
            # mailchimp returns a list of groups for a single mailinglist.
            # We always choose the first and return just the groups part.
            return self.mailchimp.listInterestGroupings(id=id)[0]['groups']
        except MailChimpException:
            pass

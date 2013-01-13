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
            raise

    def groups(self, list_id=None):
        """Return all available MailChimp interest groups.

        @id: the list id to connect to. e.g. u'a1346945ab'. Not the web_id!

        http://apidocs.mailchimp.com/api/rtfm/listinterestgroupings.func.php
        """
        if not list_id:
            return
        #print("MAILCHIMP LOCATOR: groups")
        self.connect()
        try:
            # mailchimp returns a list of groups for a single mailinglist.
            # We always choose the first and return just the groups part.
            return self.mailchimp.listInterestGroupings(id=list_id)[0]
        except MailChimpException, error:
            if error.code == 211:
                # "This list does not have interest groups enabled"
                # http://apidocs.mailchimp.com/api/1.3/exceptions.field.php#210-list-_-basic-actions
                return
            elif error.code == 200:
                # "Invalid MailChimp List ID"
                # http://apidocs.mailchimp.com/api/1.3/exceptions.field.php#200-list-related-errors
                return
            raise

    def subscribe(self, list_id, email_address, merge_vars, email_type):
        self.connect()
        if not email_type:
            email_type = self.settings.email_type
        try:
            self.mailchimp.listSubscribe(
                id=list_id,
                email_address=email_address,
                merge_vars=merge_vars,
                email_type=email_type,
                double_optin=self.settings.double_optin,
                update_existing=self.settings.update_existing,
                replace_interests=self.settings.replace_interests,
                send_welcome=self.settings.send_welcome
            )
        except MailChimpException:
            raise

    def account(self):
        self.connect()
        return self.mailchimp.getAccountDetails()

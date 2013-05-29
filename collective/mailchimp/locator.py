from postmonkey import PostMonkey
from collective.mailchimp.interfaces import IMailchimpSettings
from zope.component import getUtility
from postmonkey import MailChimpException
from postmonkey.exceptions import PostRequestError
from plone.registry.interfaces import IRegistry
from zope.interface import implements
from collective.mailchimp.interfaces import IMailchimpLocator


class MailchimpLocator(object):
    """Utility for MailChimp API calls.
    """

    implements(IMailchimpLocator)

    def connect(self):
        if hasattr(self, 'mailchimp'):
            return
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IMailchimpSettings)
        self.mailchimp = PostMonkey(self.settings.api_key)
        self.key_account = "collective.mailchimp.cache.account"
        self.key_groups = "collective.mailchimp.cache.groups"
        self.key_lists = "collective.mailchimp.cache.lists"

    def lists(self):
        return self.registry.get(self.key_lists, None) or self._lists()

    def _lists(self):
        #print("MAILCHIMP LOCATOR: lists")
        self.connect()
        try:
            # lists returns a dict with 'total' and 'data'. we just need data
            return self.mailchimp.lists()['data']
        except MailChimpException:
            return []
        except PostRequestError:
            return []
        except:
            raise

    def default_list_id(self):
        self.connect()
        if self.settings.default_list:
            return self.settings.default_list
        lists = self.lists()
        if len(lists) > 0:
            return lists[0]['id']

    def groups(self, list_id=None):
        if not list_id:
            return
        groups = self.registry.get(self.key_groups, {})
        return groups.get(list_id, None) or self._groups(list_id)

    def _groups(self, list_id=None):
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
        return self.registry.get(self.key_account, None) or self._account()

    def _account(self):
        self.connect()
        return self.mailchimp.getAccountDetails()

    def updateCache(self):
        self.connect()
        if not self.settings.api_key:
            return
        account = self._account()
        groups = {}
        lists = self._lists()
        for mailchimp_list in lists:
            list_id = mailchimp_list['id']
            groups[list_id] = self._groups(list_id=list_id)

        #now save this to the registry
        self.registry[self.key_account] = account
        self.registry[self.key_groups] = groups
        self.registry[self.key_lists] = tuple(lists)

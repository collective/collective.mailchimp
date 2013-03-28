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
            return []
        except PostRequestError:
            return []
        except:
            raise

    def templates(self):
        """Return all available MailChimp templates.
        http://apidocs.mailchimp.com/api/rtfm/templates.func.php
        """
        #print("MAILCHIMP LOCATOR: lists")
        self.connect()
        try:
            return self.mailchimp.templates()['user']
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

    def campaigns(self):
        self.connect()
        try:
            return self.mailchimp.campaigns()['data']
        except MailChimpException:
            return []
        except PostRequestError:
            return []
        except:
            raise

    def campaign_content(self, cid=u'8998de9be7'):
        self.connect()
        return self.mailchimp.campaignContent(cid=cid)

    def campaign_template_content(self, cid=u'8998de9be7'):
        self.connect()
        return self.mailchimp.campaignTemplateContent(cid=cid)

    def list_merge_vars(self, id='b00e4cab0e'):
        self.connect()
        return self.mailchimp.listMergeVars(id=id)
        #[{u'field_type': u'email', u'name': u'Email Address', u'show': True, u'default': u'', u'req': True, u'public': True, u'tag': u'EMAIL', u'helptext': u'', u'id': 0, u'order': u'1', u'size': u'25'}]

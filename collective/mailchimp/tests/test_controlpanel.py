import unittest2 as unittest

from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.registry import Registry

from plone.app.testing import logout

from collective.mailchimp.testing import \
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

from collective.mailchimp.interfaces import IMailchimpSettings


class TestMailchimpSettingsControlPanel(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.registry = Registry()
        self.registry.registerInterface(IMailchimpSettings)

    def test_mailchimp_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="mailchimp-settings")
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_mailchimp_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                         '@@mailchimp-settings')

    def test_mailchimp_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.failUnless('mailchimp' in [a.getAction(self)['id']
                            for a in self.controlpanel.listActions()])

    def test_record_api_key(self):
        record = self.registry.records[
            'collective.mailchimp.interfaces.IMailchimpSettings.api_key']
        self.failUnless('api_key' in IMailchimpSettings)
        self.assertEquals(record.value, u"")

    def test_record_debug(self):
        record = self.registry.records[
            'collective.mailchimp.interfaces.IMailchimpSettings.debug']
        self.failUnless('debug' in IMailchimpSettings)
        self.assertEquals(record.value, False)

    def test_record_ssl(self):
        record = self.registry.records[
            'collective.mailchimp.interfaces.IMailchimpSettings.ssl']
        self.failUnless('ssl' in IMailchimpSettings)
        self.assertEquals(record.value, True)

    def test_record_cache_sec(self):
        record = self.registry.records[
            'collective.mailchimp.interfaces.IMailchimpSettings.cache_sec']
        self.failUnless('cache_sec' in IMailchimpSettings)
        self.assertEquals(record.value, 500)

    def test_record_available_fields(self):
        record = self.registry.records[
            'collective.mailchimp.interfaces.IMailchimpSettings.available_fields']
        self.failUnless('available_fields' in IMailchimpSettings)
        # XXX: Should return vocabulary
        #self.assertEquals(record.value, None)

    def test_record_lists_email_type(self):
        record = self.registry.records[
            'collective.mailchimp.interfaces.IMailchimpSettings.lists_email_type']
        self.failUnless('lists_email_type' in IMailchimpSettings)
        self.assertEquals(record.value, 'html')

    def test_lists_double_optin(self):
        record = self.registry.records[
            'collective.mailchimp.interfaces.IMailchimpSettings.lists_double_optin']
        self.failUnless('lists_double_optin' in IMailchimpSettings)
        self.assertEquals(record.value, True)

    def test_lists_update_existing(self):
        record = self.registry.records[
            'collective.mailchimp.interfaces.IMailchimpSettings.lists_update_existing']
        self.failUnless('lists_update_existing' in IMailchimpSettings)
        self.assertEquals(record.value, False)

    def test_record_lists_replace_interests(self):
        record = self.registry.records[
            'collective.mailchimp.interfaces.IMailchimpSettings.lists_replace_interests']
        self.failUnless('lists_replace_interests' in IMailchimpSettings)
        self.assertEquals(record.value, True)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

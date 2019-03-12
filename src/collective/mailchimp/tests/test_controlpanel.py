# -*- coding: utf-8 -*-
from collective.mailchimp.interfaces import IMailchimpSettings
from collective.mailchimp.testing import (
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING,
)
from plone.app.testing import logout
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.registry import Registry
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

import unittest


class TestMailchimpSettingsControlPanel(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.registry = Registry()
        self.registry.registerInterface(IMailchimpSettings)

    def test_mailchimp_controlpanel_view(self):
        view = getMultiAdapter(
            (self.portal, self.portal.REQUEST), name="mailchimp-settings"
        )
        # view = view.__of__(self.portal)
        self.failUnless(view())

    def test_mailchimp_controlpanel_view_protected(self):
        from AccessControl import Unauthorized

        logout()
        self.assertRaises(
            Unauthorized,
            self.portal.restrictedTraverse,
            '@@mailchimp-settings',
        )

    def test_mailchimp_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.failUnless(
            'mailchimp'
            in [
                a.getAction(self)['id']
                for a in self.controlpanel.listActions()
            ]
        )

    def test_record_api_key(self):
        record = self.registry.records[
            'collective.mailchimp.interfaces.IMailchimpSettings.api_key'
        ]
        self.failUnless('api_key' in IMailchimpSettings)
        self.assertEquals(record.value, u"")


class ControlpanelFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

    def test_empty_form(self):
        self.browser.open("%s/mailchimp-settings" % self.portal_url)
        self.assertTrue("MailChimp settings" in self.browser.contents)

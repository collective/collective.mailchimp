# -*- coding: utf-8 -*-
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
import unittest2 as unittest

from collective.mailchimp.testing import \
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING


class TestNewsletterView(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_empty_form(self):
        self.browser.open("%s/newsletter" % self.portal_url)
        self.browser.getControl(name="form.buttons.subscribe").click()
        self.assertTrue("Required input is missing." in self.browser.contents)

    def test_form_with_invalid_email_address(self):
        self.browser.open("%s/newsletter" % self.portal_url)
        self.browser.getControl(name="form.widgets.email").value = \
            "Not an email address"
        self.browser.getControl(name="form.buttons.subscribe").click()
        self.assertTrue("Invalid email address" in self.browser.contents)

    def test_form_with_valid_email_address(self):
        # XXX: Not working. We need a mock mailchimp service
        #self.browser.open("%s/newsletter" % self.portal_url)
        #self.browser.getControl(name="form.widgets.email").value = \
        #    "john@doe.com"
        #self.browser.getControl(name="form.buttons.subscribe").click()
        pass


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

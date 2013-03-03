# -*- coding: utf-8 -*-
import unittest2 as unittest
from mock import patch

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser

from collective.mailchimp.testing import \
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING


class UnitTestSendAsNewsletter(unittest.TestCase):

    def setUp(self):
        from zope.publisher.browser import TestRequest
        from z3c.form.interfaces import IFormLayer
        self.context = object()
        self.request = TestRequest(
            environ={'AUTHENTICATED_USER': 'user1'},
            skin=IFormLayer
        )

    @unittest.skip("Not working")
    def test_foo(self):
        from collective.mailchimp.browser.send import SendAsNewsletter
        test_form = SendAsNewsletter(self.context, self.request)
        test_form.update()
        test_form.fields.keys()
        test_form.groups()


class IntegrationTestSendAsNewsletter(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Document', 'doc')
        self.doc = self.portal.doc
        import transaction
        transaction.commit()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

    @patch('collective.mailchimp.locator.MailchimpLocator')
    def test_form(self, mock_class):
        mock_class.templates.return_value = {
            u'user': [
                {
                    u'category': u'',
                    u'layout': u'Custom',
                    u'name': u'ACME Newsletter Template',
                    u'edit_source': True,
                    u'active': u'Y',
                    u'date_created': u'2013-01-31 15:12:22',
                    u'id': 34481,
                    u'preview_image': u'',
                },
            ]
        }
        self.browser.open("%s/doc/@@send_as_newsletter" % self.portal_url)
        self.assertTrue("Template" in self.browser.contents)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.component import getUtility

from collective.mailchimp.testing import \
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING


class MailchimpLocatorIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()

    def test_mailchimp_locator_registration(self):
        from collective.mailchimp.interfaces import IMailchimpLocator
        self.assertTrue(getUtility(IMailchimpLocator))

    def test_mailchimp_locator_connect_method(self):
        from collective.mailchimp.locator import MailchimpLocator
        locator = MailchimpLocator()
        locator.connect()
        self.assertTrue(locator.mailchimp is not False)

    def test_mailchimp_locator_lists_method(self):
        from collective.mailchimp.locator import MailchimpLocator
        locator = MailchimpLocator()
        self.assertTrue(locator.lists())
        self.assertEqual(len(locator.lists()), 2)

    def test_mailchimp_locator_groups_method(self):
        from collective.mailchimp.locator import MailchimpLocator
        locator = MailchimpLocator()
        self.assertTrue(locator.groups(list_id=u'a1346945ab'))
        self.assertEqual(
            len(locator.groups(list_id=u'a1346945ab')['groups']), 3)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

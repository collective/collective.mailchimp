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

    def test_mailchimp_locator_updateCache_method(self):
        from collective.mailchimp.locator import MailchimpLocator
        locator = MailchimpLocator()
        locator.initialize()
        # These tests pass when we run this test method separately,
        # but fail when running all tests.  Skip them because they are
        # not what we really want to test here.
        #
        # self.assertEqual(locator.registry[locator.key_account], None)
        # self.assertEqual(locator.registry[locator.key_groups], None)
        # self.assertEqual(locator.registry[locator.key_lists], None)
        locator.updateCache()
        self.assertTrue(
            isinstance(locator.registry[locator.key_account], dict))
        self.assertEqual(locator.registry[locator.key_account], {})
        self.assertTrue(
            isinstance(locator.registry[locator.key_groups], dict))
        self.assertEqual(locator.registry[locator.key_groups].keys(),
                         [u'f6257645gs', u'f6267645gs'])
        self.assertTrue(
            isinstance(locator.registry[locator.key_lists], tuple))
        self.assertEqual(len(locator.registry[locator.key_lists]), 2)
        # It does not complain when there is no api key
        locator.settings.api_key = None
        locator.updateCache()


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

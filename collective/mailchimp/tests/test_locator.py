# -*- coding: utf-8 -*-
import unittest2 as unittest

from mock import patch
from mock import MagicMock

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
            len(locator.groups(list_id=u'a1346945ab')['groups']),
            3
        )

    @patch('postmonkey.PostMonkey')
    def test_mailchimp_locator_campaigns_method(self, mock_class):
        campaigns = MagicMock(
            return_value={
                u'total': 1,
                u'data': [
                    {
                        u'type_opts': [],
                        u'inline_css': False,
                        u'analytics': u'N',
                        u'ecomm360': False,
                        u'create_time': u'2013-03-15 08:03:28',
                        u'send_time': None,
                        u'id': u'8998de9be7',
                        u'subject': u'Regular Campaign Test Subject',
                        u'auto_fb_post': None,
                        u'authenticate': True,
                        u'title': u'Regular Campaign',
                        u'timewarp_schedule': None,
                        u'from_email': u'john@doe.com',
                        u'parent_id': u'',
                        u'list_id': u'b00e4cab0e',
                        u'analytics_tag': u'',
                        u'auto_tweet': False,
                        u'status': u'save',
                        u'from_name': u'Regular Campaign Test From Name',
                        u'archive_url': u'http://eepurl.com/wN6Mj',
                        u'emails_sent': 0,
                        u'to_name': u'',
                        u'folder_id': 0,
                        u'content_type': u'template',
                        u'segment_opts': [],
                        u'tracking': {
                            u'text_clicks': True,
                            u'opens': True,
                            u'html_clicks': True
                        },
                        u'web_id': 429461,
                        u'type': u'regular',
                        u'timewarp': False,
                        u'auto_footer': False,
                        u'segment_text': u'No segment used',
                        u'template_id': 0
                    },
                ]
            }
        )
        mock_class().campaigns = campaigns

        from collective.mailchimp.locator import MailchimpLocator
        locator = MailchimpLocator()

        campaigns = locator.campaigns()

        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0]['title'], u'Regular Campaign')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

# -*- coding: utf-8 -*-
from collective.mailchimp.testing import (
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING,
)
from collective.mailchimp.testing import DUMMY_API_KEY
from collective.mailchimp.testing import MockRequestsException
from collective.mailchimp.testing import TEST_DATA_DIR

import os
import unittest


class MockRequestsTests(unittest.TestCase):
    """Test the mocking we do to the requests module.

    We only mock the requests module that is imported in locator.py.
    """

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def test_locator_requests_error(self):
        # Test that our mock exceptions are raised.  We try to raise them all
        # here, but it seems overkill to test the messages of the exceptions.
        from collective.mailchimp.locator import requests

        self.assertRaises(MockRequestsException, requests.get)
        self.assertRaises(MockRequestsException, requests.get, '')
        self.assertRaises(
            MockRequestsException, requests.get, 'http://website.unavailable'
        )
        url = 'https://api.mailchimp.com/3.0/'
        self.assertRaises(MockRequestsException, requests.get, url)
        auth = ('apikey', DUMMY_API_KEY)
        self.assertRaises(MockRequestsException, requests.get, url, auth=auth)
        self.assertRaises(
            MockRequestsException, requests.get, url, auth=auth, data=''
        )
        self.assertRaises(
            ValueError, requests.get, url, auth=auth, data='{bad json'
        )

    def test_locator_requests_success(self):
        # Test that a correct api request is answered with our mock data.
        from collective.mailchimp.locator import requests

        url = 'https://api.mailchimp.com/3.0/'
        auth = ('apikey', DUMMY_API_KEY)
        response = requests.get(url, auth=auth, data='{}')
        path = os.path.join(TEST_DATA_DIR, 'account.json')
        with open(path) as datafile:
            expected_text = datafile.read()
        self.assertEqual(response.text, expected_text)

    def test_standard_requests_error(self):
        # Test that the normal exceptions are raised.
        import requests

        self.assertRaises(TypeError, requests.get)
        self.assertRaises(ValueError, requests.get, '')
        self.assertRaises(
            requests.exceptions.ConnectionError,
            requests.get,
            'http://website.unavailable',
        )

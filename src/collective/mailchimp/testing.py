# -*- coding: utf-8 -*-
from collective.mailchimp.interfaces import IMailchimpSettings
from mock import Mock
from mock import patch
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.configuration import xmlconfig

import json
import os
import re


DUMMY_API_KEY = u"abc-us1"
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'tests', 'data')


class MockRequestsException(Exception):
    """Exception raised in the requests mock.

    This makes it easier to distinguish between exceptions of the
    original and the patched module.
    """


class MockRequests(object):
    """Class used as mock replacement for the requests module.
    """

    def __init__(self):
        self.calls = []

    @property
    def last_call(self):
        return self.calls[-1]

    @staticmethod
    def parse_arguments(*args, **kwargs):
        """Parse the arguments and return whatever we need.
        """
        if len(args) != 1:
            raise MockRequestsException(
                'Expected 1 argument, got {0}: {1}'.format(len(args), args)
            )
        # Check url
        url = args[0]
        mailchimp_url = 'api.mailchimp.com/3.0/'
        if mailchimp_url not in url:
            raise MockRequestsException(
                'Expected {0} in url {1}'.format(mailchimp_url, url)
            )
        endpoint = url.split(mailchimp_url)[1]
        # Check auth
        auth = kwargs.get('auth')
        if not auth:
            raise MockRequestsException('Expected auth in keyword arguments.')
        expected_auth = ('apikey', DUMMY_API_KEY)
        if (
            not isinstance(auth, tuple)
            or len(auth) != 2
            or expected_auth != auth
        ):
            raise MockRequestsException(
                'Expected auth {0} in keyword arguments. Got {1}'.format(
                    expected_auth, auth
                )
            )
        data = kwargs.get('data')
        # Load the data.
        if not data:
            raise MockRequestsException('Expected data in keyword arguments.')
        data = json.loads(data)
        return endpoint, data

    def post(self, *args, **kwargs):
        """This is a mock for post and get in the requests module.

        Return a json dictionary based on the end point.
        """
        endpoint, data = self.parse_arguments(*args, **kwargs)
        self.calls.append({'endpoint': endpoint, 'data': data})
        path = ''
        text = '{}'
        if not endpoint:
            path = os.path.join(TEST_DATA_DIR, 'account.json')
        elif endpoint == 'lists':
            path = os.path.join(TEST_DATA_DIR, 'lists.json')
        elif re.compile('lists/.*/interest-categories/.*/interests').match(
            endpoint
        ):
            path = os.path.join(TEST_DATA_DIR, 'interests.json')
        elif re.compile('lists/.*/interest-categories').match(endpoint):
            path = os.path.join(
                TEST_DATA_DIR, 'lists_interest_categories.json'
            )
        elif re.compile('lists/.*/members/[^/]*$').match(endpoint):
            path = os.path.join(TEST_DATA_DIR, 'member.json')
        else:
            pass
        if path:
            with open(path) as datafile:
                text = datafile.read()
        # Return mock response with text.
        return Mock(text=text)

    get = post
    put = post
    delete = post
    patch = post


class CollectiveMailchimp(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Create patcher to mock the requests module that is imported in
        # locator.py only.
        self.requests_patcher = patch(
            'collective.mailchimp.locator.requests', new_callable=MockRequests
        )
        # It looks like the patcher is started automatically, although the
        # documentation says you must start it explicitly.  Let's follow the
        # documentation.  Then we can also nicely stop it in tearDownZope.
        self.requests_patcher.start()

        # Load ZCML
        import collective.mailchimp

        xmlconfig.file(
            'configure.zcml',
            collective.mailchimp,
            context=configurationContext,
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.mailchimp:default')

        registry = getUtility(IRegistry)
        mailchimp_settings = registry.forInterface(IMailchimpSettings)
        mailchimp_settings.api_key = DUMMY_API_KEY

    def tearDownZope(self, app):
        # Undo our requests patch.
        self.requests_patcher.stop()


COLLECTIVE_MAILCHIMP_FIXTURE = CollectiveMailchimp()
COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_MAILCHIMP_FIXTURE,),
    name="CollectiveMailchimp:Integration",
)
COLLECTIVE_MAILCHIMP_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_MAILCHIMP_FIXTURE,),
    name="CollectiveMailchimp:Functional",
)

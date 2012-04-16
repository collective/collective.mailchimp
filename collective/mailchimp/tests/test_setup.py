import unittest2 as unittest

from collective.mailchimp.testing import \
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_browserlayer_available(self):
        from plone.browserlayer import utils
        from collective.mailchimp.interfaces import ICollectiveMailchimp
        self.failUnless(ICollectiveMailchimp in utils.registered_layers())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

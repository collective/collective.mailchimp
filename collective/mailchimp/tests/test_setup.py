import unittest2 as unittest

from Products.CMFCore.utils import getToolByName

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

    def test_mailchimp_css_available(self):
        cssreg = getToolByName(self.portal, "portal_css")
        stylesheets_ids = cssreg.getResourceIds()
        self.assertTrue(
            '++resource++collective.mailchimp.stylesheets/mailchimp.css'
            in stylesheets_ids
        )

    def test_mailchimp_css_enabled(self):
        cssreg = getToolByName(self.portal, "portal_css")
        self.assertTrue(
            cssreg.getResource(
                '++resource++collective.mailchimp.stylesheets/mailchimp.css'
            ).getEnabled()
        )


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

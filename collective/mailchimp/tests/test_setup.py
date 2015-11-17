# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from collective.mailchimp.testing import \
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING
from plone import api
import unittest


class TestSetup(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_product_installed(self):
        """Test if collective.mailchimp is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.mailchimp'))

    def test_browserlayer_available(self):
        from plone.browserlayer import utils
        from collective.mailchimp.interfaces import ICollectiveMailchimp
        self.assertIn(ICollectiveMailchimp, utils.registered_layers())

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

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.mailchimp'])

    def test_product_uninstalled(self):
        """Test if collective.mailchimp is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.mailchimp'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveMailchimp is removed."""
        from collective.mailchimp.interfaces import ICollectiveMailchimp
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveMailchimp, utils.registered_layers())

# -*- coding: utf-8 -*-
from collective.mailchimp.testing import (
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING,
)
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import get_installer
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestSetup(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_browserlayer_available(self):
        from plone.browserlayer import utils
        from collective.mailchimp.interfaces import ICollectiveMailchimp

        self.assertTrue(ICollectiveMailchimp in utils.registered_layers())

    def test_mailchimp_resource_bundle_available(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        from Products.CMFPlone.interfaces import IResourceRegistry

        reg = getUtility(IRegistry)
        resources = reg.collectionOfInterface(
            IResourceRegistry, prefix="plone.bundles", check=False
        )
        key = 'collective.mailchimp'
        self.assertIn(key, resources.keys())

    def test_mailchimp_css_enabled(self):
        portal_url = self.portal.absolute_url()
        css = "++resource++collective.mailchimp.stylesheets/mailchimp.css"
        # render the homepage
        html = self.portal()
        self.assertIn(css, html)


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('collective.mailchimp')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.mailchimp is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed('collective.mailchimp')
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveMailchimp is removed."""
        from collective.mailchimp.interfaces import ICollectiveMailchimp
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveMailchimp, utils.registered_layers())

    def test_mailchimp_resource_bundle_removed(self):
        from zope.component import getUtility
        from plone.registry.interfaces import IRegistry
        from Products.CMFPlone.interfaces import IResourceRegistry

        reg = getUtility(IRegistry)
        resources = reg.collectionOfInterface(
            IResourceRegistry, prefix="plone.bundles", check=False
        )
        key = 'collective.mailchimp'
        self.assertNotIn(key, resources.keys())

    def test_mailchimp_css_disabled(self):
        portal_url = self.portal.absolute_url()
        css = "++resource++collective.mailchimp.stylesheets/mailchimp.css"
        # render the homepage
        html = self.portal()
        self.assertNotIn(css, html)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

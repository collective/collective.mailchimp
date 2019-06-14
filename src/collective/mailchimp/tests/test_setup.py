# -*- coding: utf-8 -*-
from collective.mailchimp.testing import (
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING,
)
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.factory import _IMREALLYPLONE5

    _IMREALLYPLONE5  # noqa
except ImportError:
    PLONE_5 = False
else:
    PLONE_5 = True

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


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
        if not PLONE_5:
            # Plone 4
            cssreg = getToolByName(self.portal, "portal_css")
            stylesheets_ids = cssreg.getResourceIds()
            self.assertTrue(
                '++resource++collective.mailchimp.stylesheets/mailchimp.css'
                in stylesheets_ids
            )
        else:
            # Plone 5
            from zope.component import getUtility
            from plone.registry.interfaces import IRegistry
            from Products.CMFPlone.interfaces import IResourceRegistry

            reg = getUtility(IRegistry)
            resources = reg.collectionOfInterface(
                IResourceRegistry, prefix="plone.resources", check=False
            )
            key = 'resource-collective-mailchimp-stylesheets'
            self.assertIn(key, resources.keys())
            self.assertEqual(
                resources[key].css,
                ['++resource++collective.mailchimp.stylesheets/mailchimp.css'],
            )

    def test_mailchimp_css_enabled(self):
        if not PLONE_5:
            # Plone 4
            cssreg = getToolByName(self.portal, "portal_css")
            self.assertTrue(
                cssreg.getResource(
                    '++resource++collective.mailchimp.stylesheets/mailchimp.css'  # noqa
                ).getEnabled()
            )
        else:
            # Don't know how to test this in Plone 5.
            pass


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.mailchimp'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.mailchimp is cleanly uninstalled."""
        self.assertFalse(
            self.installer.isProductInstalled('collective.mailchimp')
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveMailchimp is removed."""
        from collective.mailchimp.interfaces import ICollectiveMailchimp
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveMailchimp, utils.registered_layers())


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

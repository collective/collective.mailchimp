# -*- coding: utf-8 -*-
from collective.mailchimp.testing import (
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING,
)
from Products.CMFCore.utils import getToolByName

import unittest


try:
    from Products.CMFPlone.factory import _IMREALLYPLONE5

    _IMREALLYPLONE5  # noqa
except ImportError:
    PLONE_5 = False
else:
    PLONE_5 = True


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


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

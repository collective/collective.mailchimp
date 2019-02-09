# -*- coding: utf-8 -*-
from collective.mailchimp.browser import portlet as mailchimp
from collective.mailchimp.testing import (
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING,
)
from plone.app.portlets.storage import PortletAssignmentMapping
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType
from plone.testing.z2 import Browser
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.site.hooks import setHooks

import unittest


class TestPortlet(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        setHooks()

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='portlet.MailChimp')
        self.assertEquals(portlet.addview, 'portlet.MailChimp')

    def testInterfaces(self):
        portlet = mailchimp.Assignment(name="foo")
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name='portlet.MailChimp')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn'
        )
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], mailchimp.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.portal.REQUEST

        mapping['foo'] = mailchimp.Assignment(name="foo")
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, mailchimp.EditForm))

    def testRenderer(self):
        context = self.portal
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.leftcolumn', context=self.portal
        )
        assignment = mailchimp.Assignment(name="foo")

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer
        )
        self.failUnless(isinstance(renderer, mailchimp.Renderer))


class TestRenderer(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        setHooks()
        # Make sure News Items use simple_publication_workflow
        self.portal.portal_workflow.setChainForPortalTypes(
            ['News Item'], ['simple_publication_workflow']
        )

    def renderer(
        self,
        context=None,
        request=None,
        view=None,
        manager=None,
        assignment=None,
    ):
        context = context or self.portal
        request = request or self.portal.REQUEST
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.leftcolumn', context=self.portal
        )
        assignment = assignment or mailchimp.Assignment(
            template='portlet_recent', macro='portlet'
        )

        return getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer
        )


class TestPortletIntegration(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()

        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD),
        )

    def test_add_portlet_form(self):
        self.browser.open(
            self.portal_url
            + "/++contextportlets++plone.leftcolumn/+/portlet.MailChimp"
        )

        self.assertTrue("Add MailChimp Portlet" in self.browser.contents)
        self.assertTrue("Title" in self.browser.contents)
        self.assertTrue("Available lists" in self.browser.contents)
        self.assertTrue("ACME Newsletter" in self.browser.contents)
        self.assertTrue("ACME Newsletter 2" in self.browser.contents)

    def test_add_portlet(self):
        self.browser.open(
            self.portal_url
            + "/++contextportlets++plone.leftcolumn/+/portlet.MailChimp"
        )
        self.browser.getControl("Title").value = "ACME Newsletter Portlet"
        self.browser.getControl(
            name="form.widgets.available_lists:list", index=0
        ).value = ["f6257645gs"]
        self.browser.getControl("Save").click()

        self.assertEqual(
            self.browser.url, self.portal_url + '/@@manage-portlets'
        )
        self.assertTrue("Hide" in self.browser.contents)
        self.assertTrue("MailChimp" in self.browser.contents)

        self.browser.open(self.portal_url)
        self.assertTrue("ACME Newsletter Portlet" in self.browser.contents)
        self.assertTrue("Email address" in self.browser.contents)

    def test_edit_portlet(self):
        # Create portlet
        self.browser.open(
            self.portal_url
            + "/++contextportlets++plone.leftcolumn/+/portlet.MailChimp"
        )
        self.browser.getControl("Title").value = "ACME Newsletter Portlet"
        self.browser.getControl(
            name="form.widgets.available_lists:list", index=0
        ).value = ["f6257645gs"]
        self.browser.getControl("Save").click()
        # Edit portlet
        self.browser.open(
            self.portal_url
            + "/++contextportlets++plone.leftcolumn/mailchimp/edit"
        )
        self.browser.getControl("Title").value = "Lorem Ipsum"
        self.browser.getControl(
            name="form.widgets.available_lists:list", index=0
        ).value = ["f6267645gs"]
        self.browser.getControl("Save").click()

        self.browser.open(
            self.portal_url
            + "/++contextportlets++plone.leftcolumn/mailchimp/edit"
        )
        self.assertTrue("Lorem Ipsum" in self.browser.contents)
        self.browser.open(self.portal_url)
        self.assertTrue("Lorem Ipsum" in self.browser.contents)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

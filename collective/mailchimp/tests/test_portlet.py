# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone.testing.z2 import Browser
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import setRoles
from zope.component import getUtility, getMultiAdapter
from zope.site.hooks import setHooks

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from collective.mailchimp.portlets import mailchimp as news
from collective.mailchimp.testing import \
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING


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
        portlet = news.Assignment(count=5)
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name='portlet.MailChimp')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], news.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.portal.REQUEST

        mapping['foo'] = news.Assignment(count=5)
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, news.EditForm))

    def testRenderer(self):
        context = self.portal
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager,
            name='plone.leftcolumn', context=self.portal)
        assignment = news.Assignment(count=5)

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment),
            IPortletRenderer)
        self.failUnless(isinstance(renderer, news.Renderer))


class TestRenderer(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        setHooks()
        # Make sure News Items use simple_publication_workflow
        self.portal.portal_workflow.setChainForPortalTypes(
            ['News Item'], ['simple_publication_workflow'])

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.portal
        request = request or self.portal.REQUEST
        view = view or self.portal.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager,
            name='plone.leftcolumn',
            context=self.portal)
        assignment = assignment or news.Assignment(
            template='portlet_recent',
            macro='portlet')

        return getMultiAdapter(
            (context, request, view, manager, assignment),
            IPortletRenderer)

#    def test_published_news_items(self):
#        setRoles(self.portal, TEST_USER_ID, ['Manager'])
#        self.portal.invokeFactory('News Item', 'n1')
#        self.portal.invokeFactory('News Item', 'n2')
#        self.portal.portal_workflow.doActionFor(self.portal.n1, 'publish')
#
#        r = self.renderer(
#            assignment=news.Assignment(count=5, state=('draft', )))
#        self.assertEquals(0, len(r.published_news_items()))
#        r = self.renderer(
#            assignment=news.Assignment(count=5, state=('published', )))
#        self.assertEquals(1, len(r.published_news_items()))
#        r = self.renderer(
#            assignment=news.Assignment(
#                count=5, state=('published', 'private', )))
#        self.assertEquals(2, len(r.published_news_items()))

#    def test_all_news_link(self):
#        if 'news' in self.portal:
#            self.portal._delObject('news')
#        r = self.renderer(assignment=news.Assignment(count=5))
#        self.assertEqual(r.all_news_link(), None)
#        setRoles(self.portal, TEST_USER_ID, ['Manager'])
#        self.portal.invokeFactory('Folder', 'news')
#        self.failUnless(r.all_news_link().endswith('/news'))


class TestPortletIntegration(unittest.TestCase):

    layer = COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal_url = self.portal.absolute_url()

        from mocker import Mocker
        mocker = Mocker()
        obj = mocker.replace("greatape.MailChimp")
        obj("foo", "bar")()
        mocker.result([{
            u'web_id': 625,
            u'name': u'ACME Newsletter',
            u'default_from_name': u'info@acme.com',
            }])
        mocker.replay()

        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader('Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_add_portlet_form(self):
        self.browser.open(self.portal_url +
            "/++contextportlets++plone.leftcolumn/+/portlet.MailChimp")
        self.assertTrue("Add MailChimp Portlet" in self.browser.contents)
        self.assertTrue("Title" in self.browser.contents)
        self.assertTrue("Available lists" in self.browser.contents)

    def test_add_portlet(self):
        self.browser.open(self.portal_url +
            "/++contextportlets++plone.leftcolumn/+/portlet.MailChimp")
        self.browser.getControl("Title").value = "My MailChimp Portlet"
        self.assertTrue(
            self.browser.getControl(
                name="form.widgets.available_list.from").options > 0)

#    def test_edit_portlet_form(self):
#        self.browser.open(self.portal_url +
#            "/++contextportlets++plone.leftcolumn/mailchimp/edit")


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

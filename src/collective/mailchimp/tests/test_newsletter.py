# -*- coding: utf-8 -*-
from collective.mailchimp.browser.newsletter import NewsletterSubscriberForm
from collective.mailchimp.testing import (
    COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING,
)
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.z2 import Browser
from plone.z3cform.fieldsets import extensible
from zope import schema
from zope.component import adapts
from zope.component import provideAdapter
from zope.interface import Interface
from zope.interface import Invalid

import unittest


def validate(value):
    if value is not True:
        raise Invalid(u'Required test field not checked')
    return True


class ITestExtenderSchema(Interface):

    accept = schema.Bool(title=u'accept', required=True, constraint=validate)


class TestExtender(extensible.FormExtender):
    adapts(Interface, Interface, NewsletterSubscriberForm)

    def update(self):
        self.add(ITestExtenderSchema)


class TestNewsletterView(unittest.TestCase):

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

    def test_empty_form(self):
        self.browser.open("%s/newsletter" % self.portal_url)
        self.browser.getControl(name="form.buttons.subscribe").click()
        self.assertTrue("Required input is missing." in self.browser.contents)

    def test_form_with_invalid_email_address(self):
        self.browser.open("%s/newsletter" % self.portal_url)
        self.browser.getControl(
            name="form.widgets.email"
        ).value = "Not an email address"
        self.browser.getControl(name="form.buttons.subscribe").click()
        self.assertTrue("Invalid email address" in self.browser.contents)


class TestNewsletterExtender(unittest.TestCase):

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
        provideAdapter(factory=TestExtender)

    def test_newsletter_extender(self):
        self.browser.open("%s/newsletter" % self.portal_url)
        self.browser.getControl(
            name="form.widgets.email"
        ).value = "valid@email.com"
        self.browser.getControl(name="form.buttons.subscribe").click()
        self.assertTrue(
            "Required test field not checked" in self.browser.contents
        )


#    def test_form_with_valid_email_address(self):
#        self.browser.open("%s/newsletter" % self.portal_url)
#        self.browser.getControl(name="form.widgets.email").value = \
#            "john@doe.com"
#        self.browser.getControl(name="form.buttons.subscribe").click()

#    def test_form_with_already_subscribed_email_address(self):
#        # Subscribe once
#        self.browser.open("%s/newsletter" % self.portal_url)
#        self.browser.getControl(name="form.widgets.email").value = \
#            "john@doe.com"
#        self.browser.getControl(name="form.buttons.subscribe").click()
#        # Subscribe twice
#        self.browser.open("%s/newsletter" % self.portal_url)
#        self.browser.getControl(name="form.widgets.email").value = \
#            "john@doe.com"
#        self.browser.getControl(name="form.buttons.subscribe").click()

#    def test_form_with_banned_email_address(self):
#        self.browser.open("%s/newsletter" % self.portal_url)
#        self.browser.getControl(name="form.widgets.email").value = \
#            "john@doe.com"
#        self.browser.getControl(name="form.buttons.subscribe").click()


class TestUnsubscribeNewsletterView(unittest.TestCase):

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

    def test_empty_form(self):
        self.browser.open("%s/unsubscribe-newsletter" % self.portal_url)
        self.browser.getControl(name="form.buttons.unsubscribe").click()
        self.assertTrue("Required input is missing." in self.browser.contents)

    def test_form_with_email_address(self):
        self.browser.open("%s/unsubscribe-newsletter" % self.portal_url)
        self.browser.getControl(
            name="form.widgets.email"
        ).value = "freddy@freddiesjokes.com"
        unsub_all_checkbox = self.browser.getControl(
            name='form.widgets.unsubscribe:list', index=0
        )
        unsub_all_checkbox.value = ['checked']
        self.browser.getControl(name="form.buttons.unsubscribe").click()

        from collective.mailchimp.locator import requests

        self.assertEqual(
            requests.last_call,
            {
                'endpoint': (
                    u'lists/f6257645gs/members/'
                    u'06f12badc3b5fffc57576822131ded7c'
                ),
                'data': {u'status': u'unsubscribed'},
            },
        )


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

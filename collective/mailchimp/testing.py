# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.registry.interfaces import IRegistry
from plone.testing import z2
from zope.configuration import xmlconfig
from zope.component import getUtility

from collective.mailchimp.interfaces import IMailchimpSettings
import collective.mailchimp


class CollectiveMailchimp(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.mailchimp)        

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.mailchimp:default')
        registry = getUtility(IRegistry)
        mailchimp_settings = registry.forInterface(IMailchimpSettings)
        mailchimp_settings.api_key = u"abcdefg-us2"


COLLECTIVE_MAILCHIMP_FIXTURE = CollectiveMailchimp()

COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_MAILCHIMP_FIXTURE,),
    name='CollectiveMailchimp:IntegrationTesting'
)

COLLECTIVE_MAILCHIMP_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_MAILCHIMP_FIXTURE,),
    name='CollectiveMailchimp:FunctionalTesting'
)

COLLECTIVE_MAILCHIMP_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_MAILCHIMP_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveMailchimp:AcceptanceTesting'
)

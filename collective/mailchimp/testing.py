from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig


class CollectiveMailchimp(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.mailchimp
        xmlconfig.file('configure.zcml',
                       collective.mailchimp,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.mailchimp:default')

COLLECTIVE_MAILCHIMP_FIXTURE = CollectiveMailchimp()
COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_MAILCHIMP_FIXTURE,),
    name="CollectiveMailchimp:Integration")
COLLECTIVE_MAILCHIMP_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_MAILCHIMP_FIXTURE,),
    name="CollectiveMailchimp:Functional")

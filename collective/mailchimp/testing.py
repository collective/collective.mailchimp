from collective.mailchimp.interfaces import IMailchimpSettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig


class CollectiveMailchimp(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        from mocker import Mocker
        from mocker import ANY
        mocker = Mocker()
        postmonkey = mocker.replace("postmonkey")
        mailchimp = postmonkey.PostMonkey(ANY)
        mocker.count(0, 1000)
        # Lists
        mailchimp.lists()
        mocker.count(0, 1000)
        mocker.result({
            u'total': 2,
            u'data': [{
                    u'id': 625,
                    u'web_id': 625,
                    u'name': u'ACME Newsletter',
                    u'default_from_name': u'info@acme.com',
                },
                {
                    u'id': 626,
                    u'web_id': 626,
                    u'name': u'ACME Newsletter 2',
                    u'default_from_name': u'info@acme.com',
                },
            ]})
        # Get account details
        mailchimp.getAccountDetails()
        mocker.count(0, 1000)
        mocker.result([])
        result = {
            u'total': 1,
            u'data': [{
                u'use_awesomebar': True,
                u'beamer_address': u'NWVmY2ZkYjjNjc=@campaigns.mailchimp.com',
                u'web_id': 17241,
                u'name': u'Test Newsletter',
                u'email_type_option': False,
                u'modules': [],
                u'default_language': u'de',
                u'default_from_name': u'Timo Stollenwerk',
                u'visibility': u'pub',
                u'subscribe_url_long':
                    u'http://johndoe.us4.list-manage1.com/subscribe?u=5e&id=fd',
                u'default_subject': u'Test Newsletter',
                u'subscribe_url_short': u'http://eepurl.com/h6Rjg',
                u'default_from_email': u'no-reply@timostollenwerk.net',
                u'date_created': u'2011-12-27 16:15:03',
                u'list_rating': 0,
                u'id': u'fdd8e33870',
                u'stats': {
                    u'grouping_count': 0,
                    u'open_rate': None,
                    u'member_count': 0,
                    u'click_rate': None,
                    u'cleaned_count_since_send': 0,
                    u'member_count_since_send': 0,
                    u'target_sub_rate': None,
                    u'group_count': 0,
                    u'avg_unsub_rate': None,
                    u'merge_var_count': 2,
                    u'unsubscribe_count': 0,
                    u'cleaned_count': 0,
                    u'avg_sub_rate': None,
                    u'unsubscribe_count_since_send': 0,
                    u'campaign_count': 1
                    }
                }
            ]}

        mocker.replay()

        # Load ZCML
        import collective.mailchimp
        xmlconfig.file('configure.zcml',
                       collective.mailchimp,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.mailchimp:default')

        registry = getUtility(IRegistry)
        mailchimp_settings = registry.forInterface(IMailchimpSettings)
        mailchimp_settings.api_key = u"abc"

COLLECTIVE_MAILCHIMP_FIXTURE = CollectiveMailchimp()
COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_MAILCHIMP_FIXTURE,),
    name="CollectiveMailchimp:Integration")
COLLECTIVE_MAILCHIMP_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_MAILCHIMP_FIXTURE,),
    name="CollectiveMailchimp:Functional")

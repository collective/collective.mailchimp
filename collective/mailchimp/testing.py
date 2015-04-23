from collective.mailchimp.interfaces import IMailchimpSettings
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from postmonkey import MailChimpException
from zope.configuration import xmlconfig


# We use mocker.  In one layer we want to change the result given back
# by calling a function.  In a second layer we instead want to raise
# an exception.  If you do that with 'mocker.result = result' and
# 'mocker.throw(Exception()', the two approaches bite each other: the
# first one wins, so it is active in both layers.  So: in both layers
# we use 'mocker.call' and that solves our problem: the previous mock
# call is overridden.  Well, that is the theory.


def raise_exc_code(code):
    # Return a function that raises an exception with this code.
    def fun(*args, **kwargs):
        raise MailChimpException(code, 'Some MailChimp error')
    return fun


def return_result(result):
    # Return a function that returns this result.
    def fun(*args, **kwargs):
        return result
    return fun


class CollectiveMailchimp(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        from mocker import Mocker
        from mocker import ANY
        from mocker import KWARGS
        mocker = Mocker()
        postmonkey = mocker.replace("postmonkey")
        mailchimp = postmonkey.PostMonkey(ANY)
        mocker.count(0, 1000)
        # Lists
        mailchimp.lists()
        mocker.count(0, 1000)
        result = {
            u'total': 2,
            u'data': [
                {
                    u'id': u'f6257645gs',
                    u'web_id': 625,
                    u'name': u'ACME Newsletter',
                    u'default_from_name': u'info@acme.com',
                },
                {
                    u'id': u'f6267645gs',
                    u'web_id': 626,
                    u'name': u'ACME Newsletter 2',
                    u'default_from_name': u'info@acme.com',
                },
            ]
        }
        # mocker.result = result
        mocker.call(return_result(result))

        # List Interest Groupings
        mailchimp.listInterestGroupings(KWARGS)
        mocker.count(0, 1000)
        result = [
            {
                u'groups': [
                    {
                        u'bit': u'1',
                        u'display_order': u'1',
                        u'name': u'Interest Group 1',
                        u'subscribers': 0
                    },
                    {
                        u'bit': u'2',
                        u'display_order': u'2',
                        u'name': u'Interest Group 2',
                        u'subscribers': 0
                    },
                    {
                        u'bit': u'3',
                        u'display_order': u'3',
                        u'name': u'Interest Group 3',
                        u'subscribers': 1
                    }
                ]
            }
        ]
        # mocker.result = result
        mocker.call(return_result(result))

        # Get account details
        mailchimp.getAccountDetails()
        mocker.count(0, 1000)
        result = []
        # mocker.result = result
        mocker.call(return_result(result))
        # NOTE: next result is never used.  Might want to remove it.
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
                u'id': u'f6257645gs',
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


class BadMailchimp(PloneSandboxLayer):
    # Let postmonkey throw exceptions always.

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        from mocker import Mocker
        from mocker import ANY
        from mocker import KWARGS
        mocker = Mocker()
        postmonkey = mocker.replace("postmonkey")
        mailchimp = postmonkey.PostMonkey(ANY)
        mocker.count(0, 1000)

        # Lists
        mailchimp.lists()
        mocker.count(0, 1000)
        # mocker.throw(MailChimpException(104, 'Invalid MailChimp API Key'))
        mocker.call(raise_exc_code(104))

        # List Interest Groupings
        mailchimp.listInterestGroupings(KWARGS)
        mocker.count(0, 1000)
        # mocker.throw(MailChimpException(211, 'no interest groups'))
        mocker.call(raise_exc_code(211))

        # Get account details
        mailchimp.getAccountDetails()
        mocker.count(0, 1000)
        # mocker.throw(MailChimpException(104, 'Invalid MailChimp API Key'))
        mocker.call(raise_exc_code(104))

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
        mailchimp_settings.api_key = u"invalid"

COLLECTIVE_MAILCHIMP_FIXTURE = CollectiveMailchimp()
BAD_MAILCHIMP_FIXTURE = BadMailchimp()
COLLECTIVE_MAILCHIMP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_MAILCHIMP_FIXTURE,),
    name="CollectiveMailchimp:Integration")
COLLECTIVE_MAILCHIMP_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_MAILCHIMP_FIXTURE,),
    name="CollectiveMailchimp:Functional")
BAD_MAILCHIMP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BAD_MAILCHIMP_FIXTURE,),
    name="BadMailchimp:Integration")

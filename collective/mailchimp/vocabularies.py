from postmonkey import PostMonkey
from postmonkey import MailChimpException

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from collective.mailchimp.interfaces import IMailchimpSettings


def available_lists(context):
    registry = getUtility(IRegistry)
    mailchimp_settings = registry.forInterface(IMailchimpSettings)
    if len(mailchimp_settings.api_key) == 0:
        return SimpleVocabulary([])
    mailchimp = PostMonkey(mailchimp_settings.api_key)
    try:
        lists = mailchimp.lists()['data']
    except MailChimpException:
        pass
    except:
        return SimpleVocabulary([])
    return SimpleVocabulary([
        SimpleTerm(value=li['id'], title=li['name']) for li in lists])


def interest_groups(context):
    registry = getUtility(IRegistry)
    mailchimp_settings = registry.forInterface(IMailchimpSettings)
    if len(mailchimp_settings.api_key) == 0:
        return SimpleVocabulary([])
    mailchimp = PostMonkey(mailchimp_settings.api_key)
    try:
        # XXX: For now we fetch only the first list.
        list_id = mailchimp.lists()['data'][0]['id']
        groups = mailchimp.listInterestGroupings(id=list_id)[0]['groups']
    except MailChimpException:
        pass
    except:
        return SimpleVocabulary([])
    return SimpleVocabulary([
        SimpleTerm(
            value=group['bit'],
            title=group['name']
        ) for group in groups
    ])

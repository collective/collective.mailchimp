from greatape import MailChimp
from greatape import MailChimpError
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from collective.mailchimp.interfaces import IMailchimpSettings


def available_lists(context):
    registry = getUtility(IRegistry)
    mailchimp_settings = registry.forInterface(IMailchimpSettings)
    mailchimp = MailChimp(
        mailchimp_settings.api_key,
        mailchimp_settings.ssl,
        mailchimp_settings.debug)
    try:
        lists = mailchimp(method='lists')
    except MailChimpError:
        pass
    except:
        return SimpleVocabulary([])
    return SimpleVocabulary([
        SimpleTerm(value=li['id'], title=li['name']) for li in lists])

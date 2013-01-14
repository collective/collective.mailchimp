from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.mailchimp.interfaces import IMailchimpSettings


def update_registry(context):
    registry = getUtility(IRegistry)
    registry.registerInterface(IMailchimpSettings)

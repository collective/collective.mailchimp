# -*- coding: utf-8 -*-
from collective.mailchimp.interfaces import IMailchimpSettings
from plone.app.upgrade.utils import loadMigrationProfile
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility


PROFILE_ID = "profile-collective.mailchimp:default"


def update_registry(context):
    registry = getUtility(IRegistry)
    registry.registerInterface(IMailchimpSettings)


def install_mailchimp_stylesheet(context):
    csstool = getToolByName(context, 'portal_css', None)
    if csstool is None:
        return
    stylesheet_id = (
        '++resource++collective.mailchimp.stylesheets/mailchimp.css'
    )
    if stylesheet_id not in csstool.getResourceIds():
        csstool.manage_addStylesheet(
            id=stylesheet_id,
            rel='stylesheet',
            rendering='link',
            enabled=True,
            cookable=True,
        )


def install_mailchimp_cache(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')


def reload_profile(context):
    loadMigrationProfile(context, 'profile-collective.mailchimp:default')


def add_max_lists_number_setting(context):
    registry = getUtility(IRegistry)
    # we need to omit other fields because vocabularies (ex: available_lists)
    # use our new (not existing) field and cause traceback
    registry.registerInterface(
        IMailchimpSettings,
        omit=(
            'api_key',
            'default_list',
            'double_optin',
            'email_type',
            'email_type_is_optional',
            'replace_interests',
            'send_welcome',
            'update_existing',
        ),
    )

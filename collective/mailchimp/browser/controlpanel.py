from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import greatape
from z3c.form import validator

from plone.app.registry.browser import controlpanel

from collective.mailchimp.interfaces import IMailchimpSettings
from collective.mailchimp import _


class MailchimpSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IMailchimpSettings
    label = _(u"MailChimp settings")
    description = _(u"""""")

    def updateFields(self):
        super(MailchimpSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(MailchimpSettingsEditForm, self).updateWidgets()


class MailchimpSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = MailchimpSettingsEditForm
    index = ViewPageTemplateFile('controlpanel.pt')

    def mailchimp_account(self):
        registry = getUtility(IRegistry)
        mailchimp_settings = registry.forInterface(IMailchimpSettings)
        mailchimp = greatape.MailChimp(
            mailchimp_settings.api_key,
            mailchimp_settings.ssl,
            mailchimp_settings.debug)
        return mailchimp(method='getAccountDetails')

    def available_lists(self):
        registry = getUtility(IRegistry)
        mailchimp_settings = registry.forInterface(IMailchimpSettings)
        mailchimp = greatape.MailChimp(
            mailchimp_settings.api_key,
            mailchimp_settings.ssl,
            mailchimp_settings.debug)
        try:
            return mailchimp(method='lists')
        except:
            pass

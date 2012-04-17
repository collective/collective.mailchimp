from zope.interface import Invalid
from z3c.form.interfaces import WidgetActionExecutionError
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import greatape

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
        try:
            return mailchimp(method='getAccountDetails')
        except greatape.MailChimpError, error:
            raise WidgetActionExecutionError(
                Invalid(u"Could not fetch account details from MailChimp. " +
                    "Please check your MailChimp API key: %s" % error))

    def available_lists(self):
        registry = getUtility(IRegistry)
        mailchimp_settings = registry.forInterface(IMailchimpSettings)
        mailchimp = greatape.MailChimp(
            mailchimp_settings.api_key,
            mailchimp_settings.ssl,
            mailchimp_settings.debug)
        try:
            return mailchimp(method='lists')
        except greatape.MailChimpError, error:
            raise WidgetActionExecutionError(
                Invalid(u"Could not fetch available lists from MailChimp. " +
                    "Please check your MailChimp API key: %s" % error))

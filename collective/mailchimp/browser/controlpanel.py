from zope.interface import Invalid
from z3c.form.interfaces import WidgetActionExecutionError
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from postmonkey import PostMonkey
from postmonkey import MailChimpException

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
        if len(mailchimp_settings.api_key) == 0:
            return []
        mailchimp = PostMonkey(mailchimp_settings.api_key)
        try:
            return mailchimp.getAccountDetails()
        except MailChimpException, error:
            raise WidgetActionExecutionError(
                Invalid(u"Could not fetch account details from MailChimp. " +
                    "Please check your MailChimp API key: %s" % error))

    def available_lists(self):
        registry = getUtility(IRegistry)
        mailchimp_settings = registry.forInterface(IMailchimpSettings)
        mailchimp = PostMonkey(mailchimp_settings.api_key)
        try:
            return mailchimp.lists()
        except MailChimpException, error:
            raise WidgetActionExecutionError(
                Invalid(u"Could not fetch available lists from MailChimp. " +
                    "Please check your MailChimp API key: %s" % error))

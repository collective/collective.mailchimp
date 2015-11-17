from zope.interface import Invalid
from z3c.form.interfaces import WidgetActionExecutionError
from zope.component import getUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ..exceptions import (
    PostRequestError,
    MailChimpException
)

from plone.app.registry.browser import controlpanel
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

from collective.mailchimp.interfaces import IMailchimpSettings
from collective.mailchimp.interfaces import IMailchimpLocator
from collective.mailchimp import _


class MailchimpSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IMailchimpSettings
    label = _(u"MailChimp settings")
    description = _(u"""""")

    def update(self):
        self.updateCache()
        super(MailchimpSettingsEditForm, self).update()

    def updateFields(self):
        super(MailchimpSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(MailchimpSettingsEditForm, self).updateWidgets()

    def updateCache(self):
        mailchimp = getUtility(IMailchimpLocator)
        mailchimp.updateCache()


class MailchimpSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = MailchimpSettingsEditForm
    index = ViewPageTemplateFile('controlpanel.pt')

    def mailchimp_account(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        mailchimp = getUtility(IMailchimpLocator)
        try:
            return mailchimp.account()
        except PostRequestError:
            return []
        except MailChimpException, error:
            raise WidgetActionExecutionError(
                Invalid(
                    u"Could not fetch account details from MailChimp. " +
                    u"Please check your MailChimp API key: %s" % error
                )
            )

    def available_lists(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        mailchimp = getUtility(IMailchimpLocator)
        try:
            return mailchimp.lists()
        except MailChimpException, error:
            raise WidgetActionExecutionError(
                Invalid(
                    u"Could not fetch available lists from MailChimp. " +
                    u"Please check your MailChimp API key: %s" % error
                )
            )

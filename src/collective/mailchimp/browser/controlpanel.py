# -*- coding: utf-8 -*-
from ..exceptions import MailChimpException
from ..exceptions import PostRequestError
from collective.mailchimp import _
from collective.mailchimp.interfaces import IMailchimpLocator
from collective.mailchimp.interfaces import IMailchimpSettings
from plone.app.registry.browser import controlpanel
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.interfaces import WidgetActionExecutionError
from zope.component import getUtility
from zope.interface import alsoProvides
from zope.interface import Invalid


try:
    from plone.protect.interfaces import IDisableCSRFProtection
except ImportError:
    # BBB for old plone.protect, default until at least Plone 4.3.7.
    IDisableCSRFProtection = None


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
        if IDisableCSRFProtection is not None:
            alsoProvides(self.request, IDisableCSRFProtection)
        mailchimp = getUtility(IMailchimpLocator)
        try:
            return mailchimp.account()
        except PostRequestError:
            return []
        except MailChimpException as error:
            raise WidgetActionExecutionError(
                Invalid(
                    u"Could not fetch account details from MailChimp. "
                    + u"Please check your MailChimp API key: %s" % error
                )
            )

    def available_lists(self):
        if IDisableCSRFProtection is not None:
            alsoProvides(self.request, IDisableCSRFProtection)
        mailchimp = getUtility(IMailchimpLocator)
        try:
            return mailchimp.lists()
        except MailChimpException as error:
            raise WidgetActionExecutionError(
                Invalid(
                    u"Could not fetch available lists from MailChimp. "
                    + u"Please check your MailChimp API key: %s" % error
                )
            )

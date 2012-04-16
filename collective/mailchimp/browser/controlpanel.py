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

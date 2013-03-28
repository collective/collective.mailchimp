from z3c.form import button
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from zope.interface import alsoProvides

from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from plone.autoform.form import AutoExtensibleForm

from collective.mailchimp.interfaces import ISendable
from collective.mailchimp.interfaces import ISendAsNewsletter
from collective.mailchimp import _


class SendAsNewsletter(AutoExtensibleForm, form.EditForm):
    schema = ISendAsNewsletter
    id = "send-as-newsletter"
    label = _(u'Send as newsletter')
    description = _(u"")
    form_name = _(u'Send as newsletter')
    ignoreContext = True

    def updateFields(self):
        super(SendAsNewsletter, self).updateFields()
        self.fields['mailinglist'].widgetFactory = \
            CheckBoxFieldWidget
        self.fields['campaigns'].widgetFactory = \
            CheckBoxFieldWidget
        self.fields['interest_groups'].widgetFactory = \
            CheckBoxFieldWidget

    @button.buttonAndHandler(_(u'Send'), name='send')
    def handle_send_action(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

    @button.buttonAndHandler(_(u'Send test email'), name='send_test')
    def handle_send_test_action(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return


class Sendable(BrowserView):
    """Returns True if content object has been marked as sendable.
    """
    def __call__(self):
        return ISendable.providedBy(self.context)


class MakeSendable(BrowserView):
    """View to create a print version of the content object.
    """

    def __call__(self):
        context = self.context
        request = context.REQUEST
        alsoProvides(context, ISendable)
        IStatusMessage(request).addStatusMessage(_(
            u"This document is now sendable. Click on the 'send' tab to send "
            u"it as MailChimp newsletter."
        ), type="info")
        request.response.redirect(context.absolute_url())

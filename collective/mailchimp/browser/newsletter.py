# -*- coding: utf-8 -*-
from Products.statusmessages.interfaces import IStatusMessage

from postmonkey import MailChimpException

from zope.interface import Invalid
from zope.interface import implements
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component.hooks import getSite
from zope.component import getUtility

from z3c.form import form, field, button
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.interfaces import ActionExecutionError
from z3c.form.interfaces import WidgetActionExecutionError
from z3c.form.interfaces import HIDDEN_MODE

from plone.z3cform.layout import wrap_form
from plone.z3cform.fieldsets import extensible

from collective.mailchimp import _
from collective.mailchimp.interfaces import IMailchimpLocator
from collective.mailchimp.interfaces import INewsletterSubscribe


class NewsletterSubcriber(object):
    implements(INewsletterSubscribe, IAttributeAnnotatable)
    title = u""


class NewsletterSubscriberForm(extensible.ExtensibleForm, form.Form):
    fields = field.Fields(INewsletterSubscribe)
    ignoreContext = True
    label = _(u"Subscribe to newsletter")

    def updateActions(self):
        super(NewsletterSubscriberForm, self).updateActions()
        self.actions['subscribe'].addClass('context')

    def updateFields(self):
        super(NewsletterSubscriberForm, self).updateFields()
        self.fields['interest_groups'].widgetFactory = \
            CheckBoxFieldWidget
        self.fields['email_type'].widgetFactory = \
            RadioFieldWidget

    def updateWidgets(self):
        super(NewsletterSubscriberForm, self).updateWidgets()
        if self.widgets['interest_groups'].items == []:
            self.widgets['interest_groups'].mode = HIDDEN_MODE
        self.widgets['list_id'].mode = HIDDEN_MODE
        if 'list_id' in self.context.REQUEST:
            self.widgets['list_id'].value = self.context.REQUEST['list_id']

    @button.buttonAndHandler(_(u"subscribe_to_newsletter_button",
                             default=u"Subscribe"),
                             name='subscribe')
    def handleApply(self, action):
        data, errors = self.extractData()
        if 'email' in data:
            # Fetch MailChimp settings
            mailchimp = getUtility(IMailchimpLocator)

            # Retrieve list_id either from a hidden field in the form or fetch
            # the first list from mailchimp.
            if 'list_id' in data:
                list_id = data['list_id']
            if list_id is None:
                try:
                    lists = mailchimp.lists()
                    list_id = lists[0]['id']
                except MailChimpException, error:
                    raise WidgetActionExecutionError(
                        Invalid(_(
                            u"Could not fetch list from mailchimp.com: %s" %
                            error
                        ))
                    )

            # Groupings
            if 'interest_groups' in data:
                interest_grouping = mailchimp.groups(list_id=list_id)
                if interest_grouping and data['interest_groups']:
                    data['groupings'] = [
                        {
                            'id': interest_grouping['id'],
                            'groups': ",".join(data['interest_groups']),
                        }
                    ]

            # Use email_type if one is provided by the form, if not choose the
            # default email type from the control panel settings.
            if 'email_type' in data:
                email_type = data['email_type']
            else:
                email_type = None
            # Subscribe to MailChimp list
            try:
                mailchimp.subscribe(
                    list_id=list_id,
                    email_address=data['email'],
                    merge_vars=data,
                    email_type=email_type,
                )
            except MailChimpException, error:
                if error.code == 214:
                    error_msg = _(
                        u"mailchimp_error_msg_already_subscribed",
                        default=u"Could not subscribe to newsletter. "
                                u"The email '${email}' is already subscribed.",
                        mapping={
                            u"email": data['email']
                        }
                    )
                    translated_error_msg = self.context.translate(error_msg)
                    raise WidgetActionExecutionError(
                        'email',
                        Invalid(translated_error_msg)
                    )
                elif error.code == 220:
                    error_msg = _(
                        u"mailchimp_error_msg_banned",
                        default=u"Could not subscribe to newsletter. "
                                u"The email '${email}' has been banned.",
                        mapping={
                            u"email": data['email']
                        }
                    )
                    translated_error_msg = self.context.translate(error_msg)
                    raise WidgetActionExecutionError(
                        'email',
                        Invalid(translated_error_msg)
                    )
                else:
                    error_msg = _(
                        u"mailchimp_error_msg",
                        default=u"Could not subscribe to newsletter. "
                                u"Please contact the site administrator: "
                                u"'${error}'",
                        mapping={
                            u"error": error
                        }
                    )
                    translated_error_msg = self.context.translate(error_msg)
                    raise ActionExecutionError(
                        Invalid(translated_error_msg)
                    )

            IStatusMessage(self.context.REQUEST).addStatusMessage(_(
                u"We have to confirm your email address. In order to " +
                u"finish the newsletter subscription, click on the link " +
                u"inside the email we just send you."),
                type="info"
            )
            portal = getSite()
            self.request.response.redirect(portal.absolute_url())


NewsletterView = wrap_form(NewsletterSubscriberForm)

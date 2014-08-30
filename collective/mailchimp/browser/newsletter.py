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

from plone.registry.interfaces import IRegistry
from plone.z3cform.layout import wrap_form
from plone.z3cform.fieldsets import extensible

from collective.mailchimp import _
from collective.mailchimp.interfaces import IMailchimpLocator
from collective.mailchimp.interfaces import IMailchimpSettings
from collective.mailchimp.interfaces import INewsletterSubscribe


class NewsletterSubcriber(object):
    implements(INewsletterSubscribe, IAttributeAnnotatable)
    title = u""


class NewsletterSubscriberForm(extensible.ExtensibleForm, form.Form):
    fields = field.Fields(INewsletterSubscribe)
    ignoreContext = True
    id = "newsletter-subscriber-form"
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
        # Show/hide mail format option widget
        registry = getUtility(IRegistry)
        mailchimp_settings = registry.forInterface(IMailchimpSettings)
        if not mailchimp_settings.email_type_is_optional:
            self.widgets['email_type'].mode = HIDDEN_MODE
        # Retrieve the list id either from the request/form or fall back to
        # the default_list setting.
        if 'list_id' in self.context.REQUEST:
            list_id = self.context.REQUEST['list_id']
        elif 'form.widgets.list_id' in self.request.form:
            list_id = self.request.form['form.widgets.list_id']
        else:
            list_id = mailchimp_settings.default_list
        self.widgets['list_id'].mode = HIDDEN_MODE
        self.widgets['list_id'].value = list_id
        # Show/hide interest_groups widget
        mailchimp = getUtility(IMailchimpLocator)
        groups = mailchimp.groups(list_id=list_id)
        if not groups:
            self.widgets['interest_groups'].mode = HIDDEN_MODE
        if 'preselect_group' in self.context.REQUEST:
            for group_index in self.request['preselect_group']:
                group_index = int(group_index)
                self.widgets['interest_groups']\
                    .items[group_index]['checked'] = True

    @button.buttonAndHandler(_(u"subscribe_to_newsletter_button",
                             default=u"Subscribe"),
                             name='subscribe')
    def handleApply(self, action):
        data, errors = self.extractData()
        if 'email' in data:
            mailchimp = getUtility(IMailchimpLocator)

            # Retrieve list_id either from a hidden field in the form or fetch
            # the first list from mailchimp.
            if 'list_id' in data:
                list_id = data['list_id']
            else:
                list_id = mailchimp.default_list_id()

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

# -*- coding: utf-8 -*-
from collective.mailchimp import _
from collective.mailchimp.interfaces import IMailchimpLocator
from collective.mailchimp.interfaces import IMailchimpSettings
from collective.mailchimp.interfaces import INewsletterSubscribe
from collective.mailchimp.interfaces import INewsletterUnsubscribe
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.registry.interfaces import IRegistry
from plone.z3cform.fieldsets import extensible
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_text
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.interfaces import ActionExecutionError
from z3c.form.interfaces import HIDDEN_MODE
from z3c.form.interfaces import WidgetActionExecutionError
from zExceptions import BadRequest
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Invalid

import logging
import re


logger = logging.getLogger(__name__)
# Characters that are allowed in some fields.
# This tries to prevent hacking attempts that get us blocked.
CHARS_ALLOWED = re.compile(r"^[a-zA-Z0-9\-_\./@\+]*$").match


@implementer(INewsletterSubscribe, IAttributeAnnotatable)
class NewsletterSubcriber(object):

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
        self.fields['interest_groups'].widgetFactory = CheckBoxFieldWidget
        self.fields['email_type'].widgetFactory = RadioFieldWidget

    def updateWidgets(self):
        super(NewsletterSubscriberForm, self).updateWidgets()
        widgets = self.widgets
        registry = getUtility(IRegistry)
        try:
            self.mailchimp_settings = registry.forInterface(IMailchimpSettings)
        except KeyError:
            self.mailchimp_settings = None
            return
        self.mailchimp = getUtility(IMailchimpLocator)

        # Show/hide mail format option widget
        if not self.mailchimp_settings.email_type_is_optional:
            widgets['email_type'].mode = HIDDEN_MODE

        # Retrieve the list id either from the request/form or fall back to
        # the default_list setting.
        list_id = self.context.REQUEST.get('list_id')
        list_id = list_id or self.request.form.get('form.widgets.list_id')
        list_id = list_id or self.mailchimp_settings.default_list
        widgets['list_id'].mode = HIDDEN_MODE
        widgets['list_id'].value = list_id

        # Show/hide interest_groups widget
        try:
            self.available_interest_groups = self.mailchimp.groups(list_id=list_id)
        except Exception as exc:
            logger.warning(exc)
            self.available_interest_groups = []
        if not self.available_interest_groups or \
           self.available_interest_groups.get('total_items') == 0:
            widgets['interest_groups'].mode = HIDDEN_MODE

        preselected_groups = self.request.get('preselected_group', [])
        for group_index in preselected_groups:
            group_index = int(group_index)
            widgets['interest_groups'].items[group_index]['checked'] = True

    @button.buttonAndHandler(
        _(u"subscribe_to_newsletter_button", default=u"Subscribe"),
        name='subscribe',
    )
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Retrieve list_id either from a hidden field in the form or fetch
        # the first list from mailchimp.
        list_id = data.get('list_id')
        if list_id and not CHARS_ALLOWED(list_id):
            # I saw a hacker adapt the hidden field:
            # "actual-id' UNION ALL SELECT NULL,NULL,NULL,NULL#"
            # Currently the list id is hexadecimal, but I suppose
            # we can't rely on that.
            raise BadRequest("list_id has disallowed characters")

        list_id = list_id or self.mailchimp.default_list_id()
        # list_id has to be updated for merge_fields=data to work if None
        if "list_id" in data and not data.get('list_id'):
            data['list_id'] = list_id

        # interest groups
        interests = {}
        interest_groups = data.pop('interest_groups', [])
        if self.available_interest_groups and interest_groups:
            interest_groups = map(safe_text, interest_groups)
            for group in interest_groups:
                if not CHARS_ALLOWED(group):
                    raise BadRequest("interest_groups has disallowed characters")
            # Create dictionary with as keys the interest groups, and as
            # values always True.
            interests = dict.fromkeys(interest_groups, True)
        # Use email_type if one is provided by the form, if not choose the
        # default email type from the control panel settings.
        email_type = data.get('email_type')
        if email_type and not CHARS_ALLOWED(email_type):
            raise BadRequest("email_type has disallowed characters")

        email_type = email_type or self.mailchimp_settings.email_type

        # Subscribe to MailChimp list
        try:
            self.mailchimp.subscribe(
                list_id=list_id,
                email_address=data['email'],
                email_type=email_type,
                interests=interests,
                merge_fields=data,
            )
        except Exception as error:
            return self.handle_error(error, data)

        if self.mailchimp_settings.double_optin:
            message = _(
                u"We have to confirm your email address. In order to "
                + u"finish the newsletter subscription, click on the link "
                + u"inside the email we just send you."
            )
        else:
            message = _(
                u"You have been subscribed to our newsletter succesfully."
            )

        IStatusMessage(self.context.REQUEST).addStatusMessage(
            message, type="info"
        )
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        self.request.response.redirect(site.absolute_url())

    def handle_error(self, error, data):
        # Current api v3 documentation only lists errors in the 400 and 500
        # range.  The 400 code can mean a lot of things...
        # Also, not all exceptions have a code.
        error_code = getattr(error, "code", 500)
        if error_code == 400:
            error_msg = _(
                u"mailchimp_error_msg_already_subscribed",
                default=u"Could not subscribe to newsletter. "
                u"Either the email '${email}' is already subscribed "
                u"or something else is wrong. Try again later.",
                mapping={u"email": data['email']},
            )
            translated_error_msg = self.context.translate(error_msg)
            raise WidgetActionExecutionError(
                'email', Invalid(translated_error_msg)
            )
        elif error_code == 220:
            error_msg = _(
                u"mailchimp_error_msg_banned",
                default=u"Could not subscribe to newsletter. "
                u"The email '${email}' has been banned.",
                mapping={u"email": data['email']},
            )
            translated_error_msg = self.context.translate(error_msg)
            raise WidgetActionExecutionError(
                'email', Invalid(translated_error_msg)
            )
        else:
            error_msg = _(
                u"mailchimp_error_msg",
                default=u"Could not subscribe to newsletter. "
                u"Please contact the site administrator: "
                u"'${error}'",
                mapping={u"error": error},
            )
            translated_error_msg = self.context.translate(error_msg)
            raise ActionExecutionError(Invalid(translated_error_msg))


NewsletterView = wrap_form(NewsletterSubscriberForm)  # noqa


class UnsubscribeNewsletterForm(extensible.ExtensibleForm, form.Form):

    fields = field.Fields(INewsletterUnsubscribe)
    ignoreContext = True
    id = "newsletter-unsubscriber-form"
    label = _(
        u'mailchimp_unsubscribe_newsletter_form_title',
        default=u"Unsubscribe from newsletter",
    )

    description = _(
        u'mailchimp_unsubscribe_newsletter_form_description', default=''
    )

    def updateFields(self):
        super(UnsubscribeNewsletterForm, self).updateFields()
        self.fields['interest_groups'].widgetFactory = CheckBoxFieldWidget

    def updateWidgets(self):
        super(UnsubscribeNewsletterForm, self).updateWidgets()
        registry = getUtility(IRegistry)
        self.mailchimp_settings = registry.forInterface(IMailchimpSettings)
        self.mailchimp = getUtility(IMailchimpLocator)

        # Set a given email address
        if self.request.get('email'):
            self.widgets['email'].value = self.request['email']

        # Retrieve the list id either from the request/form or fall back to
        # the default_list setting.
        list_id = self.context.REQUEST.get('list_id')
        list_id = list_id or self.request.form.get('form.widgets.list_id')
        list_id = list_id or self.mailchimp_settings.default_list
        self.widgets['list_id'].mode = HIDDEN_MODE
        self.widgets['list_id'].value = list_id

        # Show/hide interest_groups widget
        self.available_interest_groups = self.mailchimp.groups(list_id=list_id)
        if not self.available_interest_groups:
            self.widgets['interest_groups'].mode = HIDDEN_MODE

    @button.buttonAndHandler(
        _(u"unsubscribe_newsletter_button", default=u"Unsubscribe"),
        name='unsubscribe',
    )
    def handle_unsubscribe(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        list_id = data.get('list_id') or self.mailchimp.default_list_id()
        email = data['email']

        update_data = {}
        if data.get('unsubscribe'):
            update_data['status'] = 'unsubscribed'
        else:
            interest_groups = {}
            if data.get('interest_groups'):
                for group in data.get('interest_groups', []):
                    interest_groups[group] = False
                update_data['interests'] = interest_groups

        try:
            self.mailchimp.update_subscriber(
                list_id, email_address=email, **update_data
            )
        except Exception as error:
            if getattr(error, "code", 500) != 404:
                # If a subscriber did not exist we don't want to announce
                # it. Treat only != 404 as an error.
                IStatusMessage(self.request).addStatusMessage(
                    _(
                        u'mailchimp_unsubscribe_error_msg',
                        default=u'We could not unsubscribe you from '
                        u'the newsletter. '
                        u"Please contact the site administrator: "
                        u"'${error}'",
                        mapping={u"error": error},
                    ),
                    type="info",
                )

        IStatusMessage(self.request).addStatusMessage(
            _(
                u'mailchimp_unsubscribed_msg',
                default=(
                    u'Thank you. You have been unsubscribed from '
                    u'the Newsletter.'
                ),
            ),
            type="info",
        )

        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        site = getNavigationRootObject(self.context, portal)
        self.request.response.redirect(site.absolute_url())


UnsubscribeNewsletterView = wrap_form(UnsubscribeNewsletterForm)

# -*- coding: utf-8 -*-
from zope.component.hooks import getSite
from zope.interface import Invalid
from collective.mailchimp.interfaces import IMailchimpSettings

from postmonkey import PostMonkey
from postmonkey import MailChimpException

from Products.statusmessages.interfaces import IStatusMessage

from zope.component import getUtility

from z3c.form import form, field, button
from z3c.form.interfaces import WidgetActionExecutionError

from plone.z3cform.layout import wrap_form
from plone.registry.interfaces import IRegistry

from collective.mailchimp import _
from collective.mailchimp.interfaces import INewsletterSubscribe


class NewsletterSubscriberForm(form.Form):
    fields = field.Fields(INewsletterSubscribe)
    ignoreContext = True
    label = _(u"Subscribe to newsletter")

    def updateActions(self):
        super(NewsletterSubscriberForm, self).updateActions()
        self.actions['subscribe'].addClass('context')

    @button.buttonAndHandler(_(u"subscribe_to_newsletter_button",
                             default=u"Subscribe"),
                             name='subscribe')
    def handleApply(self, action):
        data, errors = self.extractData()
        if 'email' in data:
            # Fetch MailChimp settings
            registry = getUtility(IRegistry)
            mailchimp_settings = registry.forInterface(IMailchimpSettings)
            if len(mailchimp_settings.api_key) == 0:
                return
            mailchimp = PostMonkey(mailchimp_settings.api_key)

            # Fetch MailChimp lists
            # XXX, Todo: For now we just fetch the first list.
            try:
                lists = mailchimp.lists()['data']
                list_id = lists[0]['id']
            except MailChimpException, error:
                raise WidgetActionExecutionError(
                    Invalid(_(
                        u"Could not fetch list from mailchimp.com: %s" %
                        error
                    ))
                )
            # Subscribe to MailChimp list
            try:
                mailchimp.listSubscribe(
                    id=list_id,
                    email_address=data['email']
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
                elif error.code == 220:
                    error_msg = _(
                        u"mailchimp_error_msg_banned",
                        default=u"Could not subscribe to newsletter. "
                                u"The email '${email}' has been banned.",
                        mapping={
                            u"email": data['email']
                        }
                    )
                else:
                    error_msg = _(
                        u"mailchimp_error_msg_banned",
                        default=u"Could not subscribe to newsletter. "
                                u"Please contact the site administrator: "
                                u"'${error}'",
                        mapping={
                            u"error": error
                        }
                    )
                # strings need to be manually translated if they contain vars
                translated_error_msg = self.context.translate(error_msg)
                raise WidgetActionExecutionError(
                    'email',
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

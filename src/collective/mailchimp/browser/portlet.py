# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from collective.mailchimp.browser.newsletter import NewsletterSubscriberForm
from collective.mailchimp.interfaces import INewsletterSubscribe
from plone.app.portlets.portlets import base
from plone.autoform.directives import widget
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.z3cform import z2
from plone.z3cform.interfaces import IWrappedForm
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.interfaces import IFormLayer
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import alsoProvides
from zope.interface import implementer


_ = MessageFactory('collective.mailchimp')


class IMailChimpPortlet(IPortletDataProvider):

    name = schema.TextLine(
        title=_(u'Title'), description=_(u'Title of the portlet')
    )

    widget(available_lists=CheckBoxFieldWidget)
    available_lists = schema.List(
        title=_(u'Available lists'),
        description=_(u'Select available lists to subscribe to.'),
        required=True,
        min_length=1,
        value_type=schema.Choice(
            source='collective.mailchimp.vocabularies.AvailableLists'
        ),
    )


@implementer(IMailChimpPortlet)
class Assignment(base.Assignment):

    def __init__(self, name=u'', available_lists=[]):
        self.name = name
        self.available_lists = available_lists

    @property
    def title(self):
        return _(u"MailChimp")


class Renderer(base.Renderer):
    fields = field.Fields(INewsletterSubscribe)
    _template = ViewPageTemplateFile('portlet.pt')
    form = NewsletterSubscriberForm

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def render(self):
        return xhtml_compress(self._template())

    @property
    def name(self):
        return self.data.name or _(u"Subscribe to newsletter")


    def update(self):
        super(Renderer, self).update()
        self.form = NewsletterSubscriberForm(aq_inner(self.context), self.request)
        alsoProvides(self.form, IWrappedForm)
        self.form.update()


class AddForm(base.AddForm):
    schema = IMailChimpPortlet
    label = _(u"Add MailChimp Portlet")
    description = _(
        u"This portlet displays a subscription form for a "
        + u"MailChimp newsletter."
    )

    def create(self, data):
        return Assignment(
            name=data.get('name', u''),
            available_lists=data.get('available_lists', []),
        )


class EditForm(base.EditForm):
    schema = IMailChimpPortlet
    label = _(u"Edit MailChimp Portlet")
    description = _(
        u"This portlet displays a subscription form for a "
        + u"MailChimp newsletter."
    )

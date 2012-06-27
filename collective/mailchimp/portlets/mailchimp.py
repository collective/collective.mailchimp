from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.interface import implements
from zope import schema

from z3c.form import field
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize

from plone.portlets.interfaces import IPortletDataProvider

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base

from z3cformhelpers import AddForm
from z3cformhelpers import EditForm


class IMailChimpPortlet(IPortletDataProvider):

    name = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of the portlet'))

    available_lists = schema.List(
        title=_(u'Available lists'),
        description=_(u'Select available lists to subscribe to.'),
        required=True,
        min_length=1,
        value_type=schema.Choice(
            source='collective.mailchimp.vocabularies.AvailableListsVocabulary'
            )
        )


class Assignment(base.Assignment):
    implements(IMailChimpPortlet)

    def __init__(self, name=u'', available_lists=[]):
        self.name = name
        self.available_lists = available_lists

    @property
    def title(self):
        return _(u"MailChimp")


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('mailchimp.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def name(self):
        return self.data.name or _(u"Subscribe to newsletter")

    @memoize
    def _data(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(portal_type='MailChimp Item')


class AddForm(AddForm):
    fields = field.Fields(IMailChimpPortlet)
    fields['available_lists'].widgetFactory = CheckBoxFieldWidget
    label = _(u"Add MailChimp Portlet")
    description = _(
        u"This portlet displays a subscription form for a " +
        u"MailChimp newsletter.")

    def create(self, data):
        return Assignment(
            name=data.get('name'),
            available_lists=data.get('available_lists'))


class EditForm(EditForm):
    fields = field.Fields(IMailChimpPortlet)
    fields['available_lists'].widgetFactory = CheckBoxFieldWidget
    label = _(u"Edit MailChimp Portlet")
    description = _(
        u"This portlet displays a subscription form for a " +
        u"MailChimp newsletter.")

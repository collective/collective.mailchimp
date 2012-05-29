from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base


class IMailChimpPortlet(IPortletDataProvider):

    name = schema.TextLine(
        title=_(u'Title'),
        description=_(u'Title of the portlet'))

    available_list = schema.List(
        title=_(u'Available lists'),
        description=_(u'Select available lists to subscribe to.'),
        required=True,
        min_length=1,
        value_type=schema.Choice(source='raptus.mailchimp.available_list'))


class Assignment(base.Assignment):
    implements(IMailChimpPortlet)

    def __init__(self, count=5, state=('published', )):
        self.count = count
        self.state = state

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
    def available(self):
        return self.data.count > 0 and len(self._data())

    def published_news_items(self):
        return self._data()

    def all_news_link(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
            name=u'plone_portal_state')
        portal = portal_state.portal()
        if 'news' in getNavigationRootObject(context, portal).objectIds():
            return '%s/news' % portal_state.navigation_root_url()
        return None

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter((context, self.request),
            name=u'plone_portal_state')
        path = portal_state.navigation_root_path()
        limit = self.data.count
        state = self.data.state
        return catalog(portal_type='MailChimp Item',
                       review_state=state,
                       path=path,
                       sort_on='Date',
                       sort_order='reverse',
                       sort_limit=limit)[:limit]


class AddForm(base.AddForm):
    form_fields = form.Fields(IMailChimpPortlet)
    label = _(u"Add MailChimp Portlet")
    description = _(u"This portlet displays recent MailChimp Items.")

    def create(self, data):
        return Assignment(
            count=data.get('count', 5),
            state=data.get('state', ('published', )))


class EditForm(base.EditForm):
    form_fields = form.Fields(IMailChimpPortlet)
    label = _(u"Edit MailChimp Portlet")
    description = _(u"This portlet displays recent MailChimp Items.")

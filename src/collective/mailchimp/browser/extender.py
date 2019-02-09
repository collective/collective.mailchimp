# -*- coding: utf-8 -*-
from collective.mailchimp.browser.newsletter import NewsletterSubcriber
from collective.mailchimp.browser.newsletter import NewsletterSubscriberForm
from persistent import Persistent
from plone.z3cform.fieldsets import extensible
from zope import schema
from zope.annotation import factory
from zope.annotation.attribute import AttributeAnnotations
from zope.component import adapter
from zope.component import provideAdapter
from zope.interface import implementer
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IExtraBehavior(Interface):
    foo = schema.TextLine(title=u"Foo")
    bar = schema.TextLine(title=u"Bar")


@implementer(IExtraBehavior)
@adapter(NewsletterSubcriber)
class ExtraBehavior(Persistent):

    foo = u""
    bar = u""


ExtraBehavior = factory(ExtraBehavior)
provideAdapter(ExtraBehavior)
provideAdapter(AttributeAnnotations)


@adapter(Interface, IDefaultBrowserLayer, NewsletterSubscriberForm)
class ExtraBehaviorExtender(extensible.FormExtender):

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        if 'extra.foo' not in self.form.fields.keys():
            self.add(IExtraBehavior, prefix="extra")


provideAdapter(factory=ExtraBehaviorExtender, name=u"test.extender")  # noqa

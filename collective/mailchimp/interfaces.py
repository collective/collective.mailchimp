from z3c.form import interfaces

from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.akismet')


class ICollectiveMailchimp(Interface):
    """Marker interface that defines a ZTK browser layer. We can reference
    this in the 'layer' attribute of ZCML <browser:* /> directives to ensure
    the relevant registration only takes effect when this theme is installed.

    The browser layer is installed via the browserlayer.xml GenericSetup
    import step.
    """


class IMailchimpSettings(Interface):
    """Global mailchimp settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    api_key = schema.TextLine(
        title=_(u"MailChimp API Key"),
        description=_(u"help_api_key",
        default=u"Enter in your MailChimp key here."),
        required=True,
        default=u'',)

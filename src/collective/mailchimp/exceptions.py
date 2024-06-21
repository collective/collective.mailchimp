# -*- coding: utf-8 -*-


class SerializationError(Exception):
    """ Raised if a method call contains parameters that cannot be serialized to
    JSON. The object that caused the error is made available via the ``obj``
    attribute.
    """

    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return '%s could not be serialized to json' % self.obj


class DeserializationError(Exception):
    """ Raised if MailChimp responds with anything other than valid JSON.
    We use MailChimp's JSON API exclusively so it is unlikely
    that this will be raised. The response that caused the error is
    made available via the ``obj`` attribute.
    """

    def __init__(self, obj):
        self.obj = obj

    def __str__(self):
        return '%s could not be deserialized' % self.obj


class PostRequestError(Exception):
    """ If any exception is made during the POST request to MailChimp's server,
    `PostRequestError` will be raised. It wraps the underlying exception
    object and makes it available via the ``exc`` attribute.
    """

    def __init__(self, exc):
        self.exc = exc

    def __str__(self):
        return 'Caught exc "%s" with error "%s"' % (type(self.exc), self.exc)


class MailChimpException(Exception):
    """ If MailChimp returns an exception code as part of their response,
    this exception will be raised. Contains the unmodified ``code`` (int) and
    ``error`` (unicode) attributes returned by MailChimp.
    """

    def __init__(self, code, detail, errors=''):
        self.code = code
        self.detail = detail
        self.errors = errors

    def __str__(self):
        return 'MailChimp error code {0}: "{1}"\n{2}'.format(
            self.code, self.detail, self.errors
        )


class AkamaiException(MailChimpException):
    """Akamai is an provider upstream for MailChimp.

    It may give 503 code if you are blocked.  Sample:

    {'type': 'akamai_error_message', 'title': 'akamai_503', 'status': 503,
     'ref_no': 'Reference Number: ...'}
    """

    def __init__(self, code, detail, errors=''):
        self.code = code
        self.detail = detail
        self.errors = errors

    def __str__(self):
        return 'Akamai error code {0}: "{1}"\n{2}'.format(
            self.code, self.detail, self.errors
        )

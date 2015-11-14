# -*- coding: utf-8 -*-
import json
import logging
import requests
from urllib import quote
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse
from collective.mailchimp.interfaces import IMailchimpSettings
from collective.mailchimp.interfaces import IMailchimpLocator
from plone.registry.interfaces import IRegistry
from zope.interface import implements
from zope.component import getUtility
from . exceptions import (
    SerializationError,
    DeserializationError,
    PostRequestError,
    MailChimpException,
    )

_marker = object()
logger = logging.getLogger('collective.mailchimp')


class MailchimpLocator(object):
    """Utility for MailChimp API calls.
    """

    implements(IMailchimpLocator)
    key_account = "collective.mailchimp.cache.account"
    key_groups = "collective.mailchimp.cache.groups"
    key_lists = "collective.mailchimp.cache.lists"

    def __init__(self, settings={}):
        """ Use settings if provided """
        self.registry = None
        self.settings = None
        self.api_root = None
        if settings:
            self.settings = settings

    def initialize(self):
        """ Load settings from registry and construct api root"""
        if self.registry is None:
            self.registry = getUtility(IRegistry)
        if self.settings is None:
            self.settings = self.registry.forInterface(IMailchimpSettings)
        self.apikey = self.settings.api_key
        if not self.apikey:
            return
        parts = self.apikey.split('-')
        self.shard = parts[1]
        self.api_root = "https://" + self.shard + ".api.mailchimp.com/3.0/"

    def _serialize_payload(self, payload):
        """ Merges any default parameters from ``self.params`` with the
        ``payload`` (giving the ``payload`` precedence) and attempts to
        serialize the resulting ``dict`` to JSON.
        Note: MailChimp expects the JSON string to be quoted (their docs
        call it "URL encoded", but python's ``urllib`` calls it "quote").
        Raises a ``SerializationError`` if data cannot be serialized.
        """
        params = self.params.copy()
        params.update(payload)
        try:
            jsonstr = json.dumps(params)
            serialized = quote(jsonstr)
            return serialized
        except TypeError:
            raise SerializationError(payload)

    def _deserialize_response(self, text):
        """ Attempt to deserialize a JSON response from the server."""
        try:
            deserialized = json.loads(text)
        except ValueError:
            raise DeserializationError(text)
        self._fail_if_mailchimp_exc(deserialized)
        return deserialized

    def _fail_if_mailchimp_exc(self, response):
        """ If MailChimp returns an exception code and error, raise
        ``MailChimpException``. This allows callers to wrap method calls in a
        try/except clause and work with a single exception type for any
        error returned by MailChimp.
        """
        # case: response is not a dict so it cannot be an error response
        if not isinstance(response, dict):
            return
        # case: response is a dict and may be an error response
        elif 'code' in response and 'error' in response:
            raise MailChimpException(response['code'], response['error'])

    def api_request(self, endpoint='', request_type='get', **kwargs):
        """ construct the request and do a get/post.
        """
        if not self.api_root:
            return []
        headers = {'content-type': 'application/json'}
        url = urlparse.urljoin(self.api_root, endpoint)
        # we provide a json structure with the parameters.
        payload = json.dumps(kwargs)
        try:
            if request_type.lower() == 'post':
                resp = requests.post(url, auth=('apikey', self.apikey), data=payload, headers=headers)
            else:
                resp = requests.get(url, auth=('apikey', self.apikey), data=payload, headers=headers)
        except Exception, e:
            raise PostRequestError(e)
        decoded = self._deserialize_response(resp.text)
        return decoded

    def lists(self):
        """ API list call. To lower the amount of requests we use a cache
            If the cache is empty we fetch it once from the Mailchimp API.
        """
        self.initialize()
        cache = self.registry.get(self.key_lists, _marker)
        if cache and cache is not _marker:
            return cache
        return self._lists()

    def _lists(self):
        """ The actual API call for lists. """
        try:
            # lists returns a dict with 'total' and 'data'. we just need data
            response = self.api_request('lists')
        except PostRequestError:
            return []
        if 'lists' in response:
            return response['lists']
        return []

    def default_list_id(self):
        """ returns the first item in the list """
        self.initialize()
        if self.settings.default_list:
            return self.settings.default_list
        lists = self.lists()
        if len(lists) > 0:
            return lists[0]['id']

    def groups(self, list_id=None):
        """ API call for interest-categories. This is also cached. """
        if not list_id:
            return
        self.initialize()
        cache = self.registry.get(self.key_groups, _marker)
        if cache and cache is not _marker:
            groups = cache.get(list_id, _marker)
            if groups and groups is not _marker:
                return groups
        return self._groups(list_id)

    def _groups(self, list_id=None):
        """ Actual API call to Mailchimp service to get the interest categories
            for a given list.
        """
        if not list_id:
            return
        try:
            # mailchimp returns a list of groups for a single mailinglist.
            # We always choose the first and return just the groups part.
            url = 'lists/' + list_id + '/interest-categories'
            return self.api_request(url)
        except MailChimpException:
            raise

    def subscribe(self, list_id, email_address, email_type):
        """ API call to subscribe a member to a list. """
        self.initialize()
        if not email_type:
            email_type = self.settings.email_type
        try:
            endpoint = 'lists/' + list_id + '/members'
            response = self.api_request(endpoint,
                            request_type='post',
                            status='subscribed',
                            email_address=email_address,
                            email_type=email_type)
        except Exception, e:
            raise PostRequestError(e)
        except MailChimpException:
            raise
        logger.info("Subscribed %s to list with id: %s." % \
            (email_address, list_id))
        logger.debug("Subscribed %s to list with id: %s.\n\n %s" % \
            (email_address, list_id, response))
        return response

    def account(self):
        """ Get account details. This is caches as well """
        self.initialize()
        cache = self.registry.get(self.key_account, _marker)
        if cache and cache is not _marker:
            return cache
        return self._account()

    def _account(self):
        """ Actual API call to mailchimps api root.
        """
        try:
            return self.api_request()
        except MailChimpException:
            logger.exception("Exception getting account details.")
            return None

    def updateCache(self):
        """ Update cache of data from the mailchimp server.  First reset
            our mailchimp object, as the user may have picked a
            different api key.  Alternatively, compare
            self.settings.api_key and self.mailchimp.apikey.
            Connecting will recreate the mailchimp object.
        """
        self.initialize()
        if not self.settings.api_key:
            return
        # Note that we must call the _underscore methods.  These
        # bypass the cache and go directly to mailchimp, so we are
        # certain to have up to date information.
        account = self._account()
        groups = {}
        lists = self._lists()
        for mailchimp_list in lists:
            list_id = mailchimp_list['id']
            groups[list_id] = self._groups(list_id=list_id)

        # Now save this to the registry, but only if there are
        # changes, otherwise we would do a commit every time we look
        # at the control panel.
        if type(account) is dict:
            if self.registry[self.key_account] != account:
                self.registry[self.key_account] = account
        if type(groups) is dict:
            if self.registry[self.key_groups] != groups:
                self.registry[self.key_groups] = groups
        if type(lists) is list:
            lists = tuple(lists)
            if self.registry[self.key_lists] != lists:
                # Note that unfortunately this happens far too often.
                # In the 'subscribe_url_long' key of an item you can
                # easily first see:
                # 'http://edata.us3.list-manage.com/subscribe?u=abc123',
                # and a second later:
                # 'http://edata.us3.list-manage1.com/subscribe?u=abc123',
                self.registry[self.key_lists] = lists

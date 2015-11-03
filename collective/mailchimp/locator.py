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

    def __init__(self):
        self.registry = None
        self.settings = None
        self.params = {}

    def initialize(self):
        if self.registry is None:
            self.registry = getUtility(IRegistry)
        if self.settings is None:
            self.settings = self.registry.forInterface(IMailchimpSettings)
        self.apikey = self.settings.api_key
        parts = self.apikey.split('-')
        if len(parts) != 2:
            MailChimpException(response['code'], response['error'])
            print "This doesn't look like an API Key: " + self.apikey
            print "The API Key should have both a key and a server name, separated by a dash, like this: abcdefg8abcdefg6abcdefg4-us1"    
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

    def api_request(self, url, request_type='get', params={}):
        headers = {'content-type': 'application/json'}
        payload = self._serialize_payload(params)
        try:
            if request_type.lower() == 'post':
                import pdb;pdb.set_trace()
                resp = requests.post(url, auth=('apikey', self.apikey), params=payload, headers=headers)
            else:
                resp = requests.get(url, auth=('apikey', self.apikey), params=payload, headers=headers, )
        except Exception, e:
            raise PostRequestError(e)
        decoded = self._deserialize_response(resp.text)
        return decoded

    def lists(self):
        self.initialize()
        cache = self.registry.get(self.key_lists, _marker)
        if cache and cache is not _marker:
            return cache
        return self._lists()

    def _lists(self):
        try:
            # lists returns a dict with 'total' and 'data'. we just need data
            response = self.api_request(self.api_root + 'lists')
        except MailChimpException:
            return []
        except PostRequestError:
            return []
        if 'lists' in response:
            return response['lists']
        return []

    def default_list_id(self):
        self.initialize()
        if self.settings.default_list:
            return self.settings.default_list
        lists = self.lists()
        if len(lists) > 0:
            return lists[0]['id']

    def groups(self, list_id=None):
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
        if not list_id:
            return
        try:
            # mailchimp returns a list of groups for a single mailinglist.
            # We always choose the first and return just the groups part.
            url = self.api_root +'lists/' + list_id + '/interest-categories'
            return self.api_request(url)
        except MailChimpException, error:
            if error.status == 211:
                # "This list does not have interest groups enabled"
                # http://apidocs.mailchimp.com/api/1.3/exceptions.field.php#210-list-_-basic-actions
                return
            elif error.status == 200:
                # "Invalid MailChimp List ID"
                # http://apidocs.mailchimp.com/api/1.3/exceptions.field.php#200-list-related-errors
                return
            raise

    def subscribe(self, list_id, email_address, email_type):
        self.initialize()
        if not email_type:
            email_type = self.settings.email_type
        try:
            url = self.api_root + 'lists/' + list_id + '/members'
            response = self.api_request(url,
                            request_type='post',
                            params=dict(status='subscribed',
                                        email_address=str(email_address),
                                        email_type=email_type))
        except Exception, e:
            raise PostRequestError(e)
        except MailChimpException:
            raise
        logger.info(response)
        return response

    def account(self):
        self.initialize()
        cache = self.registry.get(self.key_account, _marker)
        if cache and cache is not _marker:
            return cache
        return self._account()
	
    def _account(self):
        try:
            return self.api_request(self.api_root)
        except MailChimpException:
            logger.exception("Exception getting account details.")
            return None
            
    def ping(self):
        return self.api_request(self.api_root + 'ping')


    def updateCache(self):
        # Update cache of data from the mailchimp server.  First reset
        # our mailchimp object, as the user may have picked a
        # different api key.  Alternatively, compare
        # self.settings.api_key and self.mailchimp.apikey.
        # Connecting will recreate the mailchimp object.
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

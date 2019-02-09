# -*- coding: utf-8 -*-
from .exceptions import DeserializationError
from .exceptions import MailChimpException
from .exceptions import PostRequestError
from .exceptions import SerializationError
from collective.mailchimp.interfaces import IMailchimpLocator
from collective.mailchimp.interfaces import IMailchimpSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implementer

import hashlib
import json
import logging
import requests
import six.moves


try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

_marker = object()
logger = logging.getLogger('collective.mailchimp')


@implementer(IMailchimpLocator)
class MailchimpLocator(object):
    """Utility for MailChimp API calls.
    """

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
        if not len(parts) > 1:
            # bad api key, allow to fix
            return
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
            serialized = six.moves.urllib.parse.quote(jsonstr)
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
        elif 'status' in response and 'detail' in response:
            exc = MailChimpException(
                response['status'], response['detail'], response.get('errors')
            )
            logger.warn(exc)
            raise exc

    def api_request(self, endpoint='', request_type='get', **kwargs):
        """ construct the request and do a get/post.
        """
        if not self.api_root:
            return []
        headers = {'content-type': 'application/json'}
        url = urlparse.urljoin(self.api_root, endpoint)

        # we provide a json structure with the parameters.
        payload = json.dumps(kwargs)

        assert request_type in ['get', 'post', 'put', 'delete', 'patch']
        request_method = getattr(requests, request_type)

        try:
            resp = request_method(
                url,
                auth=('apikey', self.apikey),
                data=payload,
                headers=headers,
            )
        except Exception as e:
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
        return self._groupings(list_id)

    def _groupings(self, list_id=None):
        # Return combined list of interest categories with their group options.
        # We only support one interest category per list.
        # We take the top one.
        categories = self._interest_categories(list_id)
        if not categories or not categories['categories']:
            return categories
        # We could search for the category with the highest display_order key,
        # but for a test list I made, this was zero in both interest
        # categories...  So just take the first one.
        category = categories['categories'][0]
        category_id = category.get('id')
        interests = self._interests(list_id, category_id)
        categories['interests'] = interests.get('interests', [])
        return categories

    def _interest_categories(self, list_id=None):
        """API call to Mailchimp to get interest categories.
        """
        if not list_id:
            return
        url = 'lists/' + list_id + '/interest-categories'
        try:
            return self.api_request(url)
        except MailChimpException:
            raise

    def _interests(self, list_id=None, interest_category_id=None):
        """Actual API call to Mailchimp service to get the group options.

        In api 1.3 this was given immediately with the list of interest
        categories.  In api 3.0 we need to get each interest category
        and ask for its interests/groups.
        """
        if not list_id or not interest_category_id:
            return
        url = 'lists/{0}/interest-categories/{1}/interests'.format(
            list_id, interest_category_id
        )
        try:
            return self.api_request(url)
        except MailChimpException:
            raise

    def subscribe(self, list_id, email_address, email_type, **kwargs):
        """ API call to subscribe a member to a list. """
        self.initialize()
        opt_in_status = 'subscribed'
        if self.settings.double_optin:
            opt_in_status = 'pending'
        if not email_type:
            email_type = self.settings.email_type
        endpoint = 'lists/' + list_id + '/members'
        try:
            response = self.api_request(
                endpoint,
                request_type='post',
                status=opt_in_status,
                email_address=email_address,
                email_type=email_type,
                **kwargs
            )
        except MailChimpException:
            raise
        except Exception as e:
            raise PostRequestError(e)
        logger.info(
            "Subscribed %s to list with id: %s." % (email_address, list_id)
        )
        logger.debug(
            "Subscribed %s to list with id: %s.\n\n %s"
            % (email_address, list_id, response)
        )
        return response

    def get_email_hash(self, email_address):
        return hashlib.md5(email_address).hexdigest()

    def update_subscriber(self, list_id, email_address, **kwargs):
        """API call to update a member's data"""
        self.initialize()

        email_hash = self.get_email_hash(email_address)
        endpoint = 'lists/' + list_id + '/members/' + email_hash
        try:
            response = self.api_request(
                endpoint, request_type='patch', **kwargs
            )
        except MailChimpException:
            raise
        except Exception as e:
            raise PostRequestError(e)
        logger.info(
            "Updated %s in list with id: %s." % (email_address, list_id)
        )
        logger.debug(
            "updated %s in list with id: %s.\n\n %s"
            % (email_address, list_id, response)
        )
        return response

    def get_subscriber(self, list_id, email_address, **kwargs):
        """ API call to unsubscribe a member completely from a list."""
        self.initialize()

        email_hash = self.get_email_hash(email_address)
        endpoint = 'lists/' + list_id + '/members/' + email_hash
        try:
            response = self.api_request(endpoint, request_type='get', **kwargs)
        except MailChimpException:
            raise
        except Exception as e:
            raise PostRequestError(e)
        return response

    def add_note_to_subscriber(self, list_id, email_address, note):
        """ API call to unsubscribe a member completely from a list."""
        self.initialize()

        email_hash = self.get_email_hash(email_address)
        endpoint = 'lists/' + list_id + '/members/' + email_hash + '/notes'
        try:
            response = self.api_request(
                endpoint, request_type='post', note=note
            )
        except MailChimpException:
            raise
        except Exception as e:
            raise PostRequestError(e)
        logger.info(
            "Added note for %s in list with id: %s." % (email_address, list_id)
        )
        logger.debug(
            "Added note for %s in list with id: %s.\n\n %s"
            % (email_address, list_id, response)
        )
        return response

    def account(self):
        """ Get account details. This is cached as well """
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
            groups[list_id] = self._groupings(list_id=list_id)

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

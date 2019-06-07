# -*- coding: utf-8 -*-

# Copyright 2019 Spanish National Research Council (CSIC)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy
import hashlib
import json
import logging

import requests
from six.moves.urllib import parse

from orpy import exceptions
from orpy import version


class OrpyClient(object):
    def __init__(self, url, token, debug=False):
        self.url = url
        self.token = token

        self.http_debug = debug

        self.deployments = Deployments(self)

        self._logger = logging.getLogger(__name__)

        if self.http_debug:
            # Logging level is already set on the root logger
            ch = logging.StreamHandler()
            self._logger.addHandler(ch)
            self._logger.propagate = False
            if hasattr(requests, 'logging'):
                rql = requests.logging.getLogger(requests.__name__)
                rql.addHandler(ch)
                # Since we have already setup the root logger on debug, we
                # have to set it up here on WARNING (its original level)
                # otherwise we will get all the requests logging messages
                rql.setLevel(logging.WARNING)

    def request(self, url, method, **kwargs):
        kwargs.setdefault('headers', kwargs.get('headers', {}))

        kwargs["headers"]["User-Agent"] = "orpy-%s" % version.user_agent
        kwargs["headers"]["Accept"] = "application/json"

        if self.token is not None:
            kwargs["headers"]["Authorization"] = "Bearer" + self.token

        url = parse.urljoin(self.url, url)

        self.http_log_req(method, url, kwargs)

        if method == "get":
            resp = requests.get(url, **kwargs)
        elif method == "post":
            resp = requests.post(url, **kwargs)

        self.http_log_resp(resp)

        try:
            body = resp.json()
        except Exception:
            body = None

        if resp.status_code >= 400:
            raise exceptions.from_response(resp, body, url, method)

        return resp, body

    def http_log_req(self, method, url, kwargs):
        if not self.http_debug:
            return

        string_parts = ['curl -g -i']

        if not kwargs.get('verify', True):
            string_parts.append(' --insecure')

        string_parts.append(" '%s'" % url)
        string_parts.append(' -X %s' % method)

        headers = copy.deepcopy(kwargs['headers'])
        self._redact(headers, ['Authorization'])
        # because dict ordering changes from 2 to 3
        keys = sorted(headers.keys())
        for name in keys:
            value = headers[name]
            header = ' -H "%s: %s"' % (name, value)
            string_parts.append(header)

        if 'data' in kwargs:
            data = json.loads(kwargs['data'])
            string_parts.append(" -d '%s'" % json.dumps(data))
        self._logger.debug("REQ: %s" % "".join(string_parts))

    def http_log_resp(self, resp):
        if not self.http_debug:
            return

        if resp.text and resp.status_code != 400:
            try:
                body = json.loads(resp.text)
                self._redact(body, ['access', 'token', 'id'])
            except ValueError:
                body = None
        else:
            body = None

        self._logger.debug("RESP: [%(status)s] %(headers)s\nRESP BODY: "
                           "%(text)s\n", {'status': resp.status_code,
                                          'headers': resp.headers,
                                          'text': json.dumps(body)})

    def _redact(self, target, path, text=None):
        """Replace the value of a key in `target`.

        The key can be at the top level by specifying a list with a single
        key as the path. Nested dictionaries are also supported by passing a
        list of keys to be navigated to find the one that should be replaced.
        In this case the last one is the one that will be replaced.

        :param dict target: the dictionary that may have a key to be redacted;
                            modified in place
        :param list path: a list representing the nested structure in `target`
                          that should be redacted; modified in place
        :param string text: optional text to use as a replacement for the
                            redacted key. if text is not specified, the
                            default text will be sha1 hash of the value being
                            redacted
        """

        key = path.pop()

        # move to the most nested dict
        for p in path:
            try:
                target = target[p]
            except KeyError:
                return

        if key in target:
            if text:
                target[key] = text
            elif target[key] is not None:
                # because in python3 byte string handling is ... ug
                value = target[key].encode('utf-8')
                sha1sum = hashlib.sha1(value)
                target[key] = "{SHA1}%s" % sha1sum.hexdigest()

    def _get(self, url):
        return self.request(url, "get")

    def _post(self, url, data):
        return self.request(url, "post", payload=data)

    def info(self):
        try:
            resp, body = self._get("./info")
        except exceptions.ClientException:
            raise exceptions.InvalidUrl(url=self.url)

        if resp.status_code == 200:
            return body
        else:
            raise exceptions.InvalidUrl(url=self.url)


class Deployments(object):
    def __init__(self, client):
        self.client = client

    def index(self):
        resp, body = self.client.request("./deployments", "get")
        return body["content"]

    def show(self, uuid):
        resp, body = self.client.request("./deployments/%s" % uuid,
                                         "get")
        return body

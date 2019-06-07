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

import requests
from six.moves.urllib import parse

from orpy import exceptions
from orpy import version


class OrpyClient(object):
    def __init__(self, url, token):
        self.url = url
        self.token = token

        self.deployments = Deployments(self)

    def request(self, url, method, data=None):
        headers = {
            "User-Agent": "orpy-%s" % version.__version__,
            "Accept": "application/json",
        }

        if self.token is not None:
            headers["Authorization"] = "Bearer" + self.token

        url = parse.urljoin(self.url, url)

        if method == "get":
            resp = requests.get(url, headers=headers)
        elif method == "post":
            resp = requests.post(url, payload=data, headers=headers)

        try:
            body = resp.json()
        except Exception:
            body = None

        if resp.status_code >= 400:
            raise exceptions.from_response(resp, body, url, method)

        return resp, body

    def _get(self, url):
        return self.request(url, "get")

    def _post(self, url, data):
        return self.request(url, "post", data)

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

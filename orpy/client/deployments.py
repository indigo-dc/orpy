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


class Deployments(object):
    def __init__(self, client):
        self.client = client

    def index(self):
        resp, body = self.client.get("./deployments")
        return body["content"]

    def show(self, uuid):
        resp, body = self.client.get("./deployments/%s" % uuid)
        return body

    def delete(self, uuid):
        resp, body = self.client.delete("./deployments/%s" % uuid)
        return body

    def get_template(self, uuid):
        resp, body = self.client.get("./deployments/%s/template/" % uuid)
        return body

    def create(self, template, callback_url=None, max_providers_retry=None,
               keep_last_attemp=True):
        json = {
            "template": template,
            "keepLastAttemp": keep_last_attemp,
        }
        if callback_url:
            json["callback"] = callback_url
        if max_providers_retry:
            json["maxProvidersRetry"] = max_providers_retry

        resp, body = self.client.post("./deployments/",
                                      json=json)
        return body

    def update(self, uuid, template, callback_url=None,
               max_providers_retry=None, keep_last_attemp=True):
        json = {
            "template": template,
            "keepLastAttemp": keep_last_attemp,
        }
        if callback_url:
            json["callback"] = callback_url
        if max_providers_retry:
            json["maxProvidersRetry"] = max_providers_retry

        resp, body = self.client.put("./deployments/%s" % uuid,
                                     json=json)
        return body

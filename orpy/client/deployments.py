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
    """Manage Orchestrator deployments."""

    def __init__(self, client):
        self.client = client

    def list(self):
        """List existing deployments."""
        resp, body = self.client.get("./deployments")
        return body["content"]

    def show(self, uuid):
        """Show details about a deployment.

        :param str uuid: The UUID of the deployment to show.
        """
        resp, body = self.client.get("./deployments/%s" % uuid)
        return body

    def delete(self, uuid):
        """Delete a deployment.

        :param str uuid: The UUID of the deployment to delete.
        """
        resp, body = self.client.delete("./deployments/%s" % uuid)
        return body

    def get_template(self, uuid):
        """Get the TOSCA template of a deployment.

        :param str uuid: The UUID of the deployment.
        """
        resp, body = self.client.get("./deployments/%s/template/" % uuid)
        return body

    def create(self, template, callback_url=None, max_providers_retry=None,
               keep_last_attemp=True, parameters={}):
        """Create a deployment.

        :param str template: The TOSCA template to use.
        :param str callback_url: The orchestrator callback url.
        :param int max_providers_retry: Maximum number of providers to retry.
        :param bool keep_last_attemp: Whether to keep the allocated resources
                                      in case of failure.
        """
        json = {
            "template": template,
            "keepLastAttemp": keep_last_attemp,
            "parameters": parameters,
        }
        if callback_url:
            json["callback"] = callback_url
        if max_providers_retry:
            json["maxProvidersRetry"] = max_providers_retry

        resp, body = self.client.post("./deployments/",
                                      json=json)
        return body

    def update(self, uuid, template, callback_url=None,
               max_providers_retry=None, keep_last_attemp=True,
               parameters={}):
        """Update a deployment.

        :param str uuid: The UUID of the deployment.
        :param str template: The TOSCA template to use.
        :param str callback_url: The orchestrator callback url.
        :param int max_providers_retry: Maximum number of providers to retry.
        :param bool keep_last_attemp: Whether to keep the allocated resources
                                      in case of failure.
        """
        json = {
            "template": template,
            "keepLastAttemp": keep_last_attemp,
            "parameters": parameters,
        }
        if callback_url:
            json["callback"] = callback_url
        if max_providers_retry:
            json["maxProvidersRetry"] = max_providers_retry

        resp, body = self.client.put("./deployments/%s" % uuid,
                                     json=json)
        return body

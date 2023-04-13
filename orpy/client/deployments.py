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

"""This module contains the client dealing with PaaS Orchestrator deployments."""

from orpy.client import base


class Deployments(object):
    """Manage Orchestrator deployments."""

    def __init__(self, client):
        """Initialize client.

        :params client: An instance of OrpyClient.
        """
        self.client = client

    def list(self, **kwargs):
        """List existing deployments.

        :param kwargs: Other arguments passed to the request client.

        :return: List of orpy.client.base.Deployment
        :rtype: list
        """
        resp, results = self.client.get("./deployments", **kwargs)
        return [base.Deployment(data) for data in results]

    def show(self, uuid, **kwargs):
        """Show details about a deployment.

        :param str uuid: The UUID of the deployment to show.
        :param kwargs: Other arguments passed to the request client.

        :return: The deployment requested
        :rtype: orpy.client.base.Deployment
        """
        resp, result = self.client.get("./deployments/%s" % uuid, **kwargs)
        return base.Deployment(result)

    def delete(self, uuid, **kwargs):
        """Delete a deployment.

        :param str uuid: The UUID of the deployment to delete.
        :param kwargs: Other arguments passed to the request client.

        :return: None
        :rtype: None
        """
        resp, body = self.client.delete("./deployments/%s" % uuid, **kwargs)
        return

    def get_template(self, uuid, **kwargs):
        """Get the TOSCA template of a deployment.

        :param str uuid: The UUID of the deployment.
        :param kwargs: Other arguments passed to the request client.

        :return: The TOSCA template for the deployment
        :rtype: orpy.client.base.TOSCATemplate
        """
        resp, result = self.client.get("./deployments/%s/template/" % uuid, **kwargs)
        info = {"template": result}
        return base.TOSCATemplate(info)

    def create(
        self,
        template,
        callback_url=None,
        max_providers_retry=None,
        keep_last_attemp=True,
        parameters=None,
        **kwargs,
    ):
        """Create a deployment.

        :param str template: The TOSCA template to use.
        :param str callback_url: The orchestrator callback url.
        :param int max_providers_retry: Maximum number of providers to retry.
        :param bool keep_last_attemp: Whether to keep the allocated resources
                                      in case of failure.
        :param kwargs: Other arguments passed to the request client.

        :return: The created deployment
        :rtype: orpy.client.base.Deployment
        """
        json = {
            "template": template,
            "keepLastAttemp": keep_last_attemp,
            "parameters": parameters or {},
        }
        if callback_url:
            json["callback"] = callback_url
        if max_providers_retry:
            json["maxProvidersRetry"] = max_providers_retry

        resp, result = self.client.post("./deployments/", json=json, **kwargs)
        return base.Deployment(result)

    def update(
        self,
        uuid,
        template,
        callback_url=None,
        max_providers_retry=None,
        keep_last_attemp=True,
        parameters=None,
        **kwargs,
    ):
        """Update a deployment.

        :param str uuid: The UUID of the deployment.
        :param str template: The TOSCA template to use.
        :param str callback_url: The orchestrator callback url.
        :param int max_providers_retry: Maximum number of providers to retry.
        :param bool keep_last_attemp: Whether to keep the allocated resources
                                      in case of failure.
        :param kwargs: Other arguments passed to the request client.

        :return: The updated deployment
        :rtype: orpy.client.base.Deployment
        """
        json = {
            "template": template,
            "keepLastAttemp": keep_last_attemp,
            "parameters": parameters or {},
        }
        if callback_url:
            json["callback"] = callback_url
        if max_providers_retry:
            json["maxProvidersRetry"] = max_providers_retry

        resp, result = self.client.put("./deployments/%s" % uuid, json=json, **kwargs)
        return base.Deployment(result)

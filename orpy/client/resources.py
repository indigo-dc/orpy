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

from orpy.client import base


class Resources(object):
    """Manage Orchestrator deployment resources."""

    def __init__(self, client):
        self.client = client

    def list(self, uuid):
        """List resources for a deployment.

        :param str uuid: The UUID of the deployment get the resources.

        :return: A list of orpy.client.base.Resource
        :rtype: list
        """
        resp, results = self.client.get("./deployments/%s/resources/" % uuid)
        return [base.Resource(result) for result in results]

    def show(self, deployment_uuid, resource_uuid):
        """Show details about a resource on a deployment.

        :param str resource_uuid: The UUID of the deployment get the resource.
        :param str deployment_uuid: The UUID of the resource.

        :return: The resource requested
        :rtype: orpy.client.base.Resource
        """
        resp, result = self.client.get("./deployments/%s/resources/%s" %
                                       (deployment_uuid, resource_uuid))
        return base.Resource(result)

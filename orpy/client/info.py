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
from orpy import exceptions


class Info(object):
    """Get information about the Orchestrator."""

    def __init__(self, client):
        self.client = client

    def get(self):
        """Get information about the Orchestrator.

        :return: Information about the orchestrator.
        :rtype: orpy.client.base.OrchestratorInfo
        """
        try:
            resp, body = self.client.get("./info")
        except exceptions.ClientException:
            raise exceptions.InvalidUrl(url=self.client.url)

        if resp.status_code == 200:
            body["url"] = self.client.url
            return base.OrchestratorInfo(body)
        else:
            raise exceptions.InvalidUrl(url=self.client.url)

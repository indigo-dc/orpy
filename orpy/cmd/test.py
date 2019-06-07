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


from cliff import show


class TestOrchestratorEndpoint(show.ShowOne):
    """Test if the given URL is pointing to an orchestrator.

    Use this command to check if the URL provided is actually from an INDIGO
    PaaS Orchestrator.
    """

    auth_required = False

    def take_action(self, parsed_args):
        d = self.app.client.info()
        d["url"] = self.app_args.orchestrator_url

        return self.dict2columns(d)

# -*- coding: utf-8 -*-

# Copyright 2021 Spanish National Research Council (CSIC)
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

from orpy import utils


class OrchestratorConfigShow(show.ShowOne):
    """Show current orchestrator endpoints configured.

    Use this command to get the list of endpoints that the current orchrestator
    is using.
    """

    auth_required = False

    def take_action(self, parsed_args):
        d = self.app.client.config.get().to_dict()
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = utils.format_dict(v)
        return self.dict2columns(d)


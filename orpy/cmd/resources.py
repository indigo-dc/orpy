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

from cliff import lister

from orpy import utils


class ResourcesList(lister.Lister):
    """List Resources for a given deployment."""

    def get_parser(self, prog_name):
        parser = super(ResourcesList, self).get_parser(prog_name)
        parser.add_argument('uuid',
                            metavar="<deployment uuid>",
                            help="Deployment UUID to show.")
        return parser

    def take_action(self, parsed_args):
        ret = self.app.client.resources.index(parsed_args.uuid)

        columns = (
            'uuid',
            'state',
            'toscaNodeType',
            'toscaNodeName',
            'creationTime',
            'requiredBy',
        )

        values = [utils.get_item_properties(s, columns,
                                            mixed_case_fields=columns)
                  for s in ret]

        return columns, values

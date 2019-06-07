#!/usr/bin/env python
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

import sys

from cliff import app
from cliff import command
from cliff import complete
from cliff import commandmanager
from cliff import help

from orpy import client
from orpy import exceptions
from orpy import utils
from orpy import version


class OrpyApp(app.App):
    commands = []

    def __init__(self):

        self.client = None
        self.token = None

        # Patch command.Command to add a default auth_required = True
        command.Command.auth_required = True

        # Some commands do not need authentication
        help.HelpCommand.auth_required = False
        complete.CompleteCommand.auth_required = False

        cm = commandmanager.CommandManager('orpy.cli')
        super(OrpyApp, self).__init__(
            description='INDIGO PaaS Orchestrator Python Client',
            version=version.__version__,
            command_manager=cm,
            deferred_help=True,
        )

    def initialize_app(self, argv):
        for cmd in self.commands:
            self.command_manager.add_command(cmd.__name__.lower(), cmd)
        self.token = utils.env("ORCHESTRATOR_TOKEN")
        if self.client is None:
            self.client = client.OrpyClient(self.options.orchestrator_url,
                                            self.token,
                                            debug=self.options.debug)

    def prepare_to_run_command(self, cmd):
        if cmd.auth_required and not self.token:
            raise exceptions.InvalidUsage("No token has beeen provided!")

    def build_option_parser(self, description, version):
        parser = super(OrpyApp, self).build_option_parser(
            description,
            version)

        # service token auth argument
        parser.add_argument(
            '--url',
            metavar='<orchestrator-url>',
            dest='orchestrator_url',
            default=utils.env('ORCHESTRATOR_URL'),
            help='The base url of the orchestrator rest interface. '
                 'Alternative the environment variable ORCHESTRATOR_URL '
                 'can be used.'
        )

        return parser


def main(argv=sys.argv[1:]):
    orpy = OrpyApp()
    return orpy.run(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

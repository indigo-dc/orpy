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

import argparse
import sys

from cliff import app
from cliff import command
from cliff import commandmanager
from cliff import complete
from cliff import help

from orpy.client import client
from orpy import oidc
from orpy import utils
from orpy import version


class OrpyApp(app.App):
    """Command line client for the INDIGO PaaS Orchestrator.

    Please, before using this command put your a valid OpenID Connnect access
    token into the ORCHESTRATOR_TOKEN environment variable, so that we can use
    this token for authentication.
    """
    commands = []

    def __init__(self):

        self.client = None
        self.token = None
        self.oidc_agent = None

        # Patch command.Command to add a default auth_required = True
        command.Command.auth_required = True

        # Some commands do not need authentication
        help.HelpCommand.auth_required = False
        complete.CompleteCommand.auth_required = False

        cm = commandmanager.CommandManager('orpy.cli')
        super(OrpyApp, self).__init__(
            description="Command line client for the INDIGO PaaS Orchestrator",
            version=version.__version__,
            command_manager=cm,
            deferred_help=True,
        )

    def initialize_app(self, argv):
        for cmd in self.commands:
            self.command_manager.add_command(cmd.__name__.lower(), cmd)
        self.token = utils.env("ORCHESTRATOR_TOKEN")

        if self.options.oidc_agent_sock and self.options.oidc_agent_account:
            self.oidc_agent = oidc.OpenIDConnectAgent(
                self.options.oidc_agent_account,
                socket_path=self.options.oidc_agent_sock
            )

        if self.client is None:
            self.client = client.OrpyClient(self.options.orchestrator_url,
                                            oidc_agent=self.oidc_agent,
                                            token=self.token,
                                            debug=self.options.debug)

    def prepare_to_run_command(self, cmd):
        if isinstance(cmd, help.HelpCommand):
            return

        if not self.options.orchestrator_url:
            self.parser.error("No URL for the orchestrator has been suplied "
                              "use --url or set the ORCHESTRATOR_URL "
                              "environment variable.")

        if cmd.auth_required:
            if (not all([self.options.oidc_agent_sock,
                         self.options.oidc_agent_account])) and not self.token:

                self.parser.error("No oidc-agent has been set up or no access "
                                  "token has been provided, please set the "
                                  "ORCHESTRATOR_TOKEN environment variable or "
                                  "set up an oidc-agent "
                                  "(see '%s help' for more details on how "
                                  "to set up authentication)" %
                                  self.parser.prog)

    def build_option_parser(self, description, version):
        auth_help = """Authentication:

    In order to interact with the INDIGO PaaS Orchestrator we need to use an
    OpenID Connect access token from a trusted OpenID Connect provider at the
    orchestrator.

    Please either store your access token in 'ORCHESTRATOR_TOKEN' or set the
    account to use with oidc-agent in the 'OIDC_ACCOUNT' and the socket path
    of the oidc-agent in the 'OIDC_SOCK' environment variable:

        export ORCHESTRATOR_TOKEN=<your access token>
            OR
        export OIDC_SOCK=<path to the oidc-agent socket>
        export OIDC_ACCOUNT=<account to use>

    Usually, the OIDC_SOCK environmental variable is already exported if you
    are using oidc-agent.

    As an alternative, you can pass the socket path and the account through
    the command line with the --oidc-agent-sock and --oidc-agent-account
    parameters.

"""
        parser = super(OrpyApp, self).build_option_parser(
            self.__doc__,
            version,
            argparse_kwargs={
                "formatter_class": argparse.RawDescriptionHelpFormatter,
                "epilog": auth_help,
            })

        parser.add_argument(
            '--oidc-agent-sock',
            metavar='<oidc-agent-socket>',
            dest='oidc_agent_sock',
            default=utils.env('OIDC_SOCK'),
            help='The path for the oidc-agent socket to use to get and renew '
                 'access tokens from the OpenID Connect provider. This '
                 'defaults to the OIDC_SOCK environment variable, that should '
                 'be automatically set up if you are using oidc-agent. '
                 'In order to use the oidc-agent you must also pass the '
                 '--oidc-agent-account parameter, or set the OIDC_ACCOUNT '
                 'environment variable.'
        )
        parser.add_argument(
            '--oidc-agent-account',
            metavar='<oidc-agent-account>',
            dest='oidc_agent_account',
            default=utils.env('OIDC_ACCOUNT'),
            help='The oidc-agent account that we will use to get tokens from. '
                 'In order to use the oidc-agent you must pass thos parameter '
                 'or set the OIDC_ACCOUNT environment variable.'
        )
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

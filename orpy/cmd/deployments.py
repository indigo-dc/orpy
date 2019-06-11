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

from cliff import command
from cliff import lister
from cliff import show

from orpy import utils


class KeyValueAction(argparse.Action):
    """A custom action to parse arguments as key=value pairs.

    Ensures that ``dest`` is a dict.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        # Make sure we have an empty dict rather than None
        if getattr(namespace, self.dest, None) is None:
            setattr(namespace, self.dest, {})

        for v in values:
            v = v.split('=', 1)
            # NOTE(qtang): Prevent null key setting in property
            if '' == v[0]:
                msg = "Property key must be specified: %s"
                raise argparse.ArgumentTypeError(msg % str(values))
            else:
                getattr(namespace, self.dest, {}).update([v])


class DeploymentList(lister.Lister):
    """List existing deployments at orchestrator."""

    # TODO(aloga): implement filters

    def take_action(self, parsed_args):
        ret = self.app.client.deployments.list()

        columns = (
            'uuid',
            'status',
            'task',
            'creationTime',
            'createdBy',
            'cloudProviderName'
        )

        values = [utils.get_item_properties(s, columns,
                                            mixed_case_fields=columns)
                  for s in ret]

        return columns, values


class DeploymentShow(show.ShowOne):
    """Show details about an existing deployment."""

    def get_parser(self, prog_name):
        parser = super(DeploymentShow, self).get_parser(prog_name)
        parser.add_argument('uuid',
                            metavar="<deployment uuid>",
                            help="Deployment UUID to show.")
        return parser

    def take_action(self, parsed_args):
        d = self.app.client.deployments.show(parsed_args.uuid).to_dict()
        d.pop("links")
        d["createdBy"] = utils.format_dict(d["createdBy"])
        return self.dict2columns(d)


class DeploymentDelete(command.Command):
    """Show details about an existing deployment."""

    def get_parser(self, prog_name):
        parser = super(DeploymentDelete, self).get_parser(prog_name)
        parser.add_argument('uuid',
                            metavar="<deployment uuid>",
                            help="Deployment UUID to delete.")
        return parser

    def take_action(self, parsed_args):
        self.app.client.deployments.delete(parsed_args.uuid)


class DeploymentGetTemplate(show.ShowOne):
    """Get template used for a given deployment."""

    def get_parser(self, prog_name):
        parser = super(DeploymentGetTemplate, self).get_parser(prog_name)
        parser.add_argument('uuid',
                            metavar="<deployment uuid>",
                            help="Deployment UUID to get template for.")
        return parser

    def take_action(self, parsed_args):
        d = self.app.client.deployments.get_template(parsed_args.uuid)
        return self.dict2columns(d.to_dict())


class DeploymentCreate(show.ShowOne):
    """Create a deployment."""

    def get_parser(self, prog_name):
        parser = super(DeploymentCreate, self).get_parser(prog_name)

        parser.add_argument("--callback-url",
                            dest="callback",
                            default=None,
                            help="The callback url.")
        parser.add_argument("--max-providers-retry",
                            dest="max_retries",
                            default=None,
                            type=int,
                            help="Maximum number of cloud providers to be "
                                 "used in case of failure (Default is to "
                                 "be unbounded).")
        parser.add_argument("--keep-last-attempt",
                            dest="keep_last",
                            default=True,
                            type=bool,
                            help="In case of failure, keep the resources "
                                 "allocated in the last try (Default: True, "
                                 "accepts boolean values).")

        parser.add_argument('filename',
                            metavar="<template file>",
                            help="TOSCA template file.")

        parser.add_argument('parameters',
                            metavar="<parameter>=<value>",
                            nargs="*",
                            action=KeyValueAction,
                            help="Input parameter for the deployment in the "
                                 "form <parameter>=<value>. Can be specified "
                                 "several times.")

        return parser

    def take_action(self, parsed_args):
        with open(parsed_args.filename, "r") as f:
            d = self.app.client.deployments.create(
                template=f.read(),
                callback_url=parsed_args.callback,
                max_providers_retry=parsed_args.max_retries,
                keep_last_attemp=parsed_args.keep_last,
                parameters=parsed_args.parameters
            )
        return self.dict2columns(d.to_dict())


class DeploymentUpdate(show.ShowOne):
    """Update an existing deployment."""

    def get_parser(self, prog_name):
        parser = super(DeploymentUpdate, self).get_parser(prog_name)

        parser.add_argument("--callback-url",
                            dest="callback",
                            default=None,
                            help="The callback url.")
        parser.add_argument("--max-providers-retry",
                            dest="max_retries",
                            default=None,
                            type=int,
                            help="Maximum number of cloud providers to be "
                                 "used in case of failure (Default is to "
                                 "be unbounded).")
        parser.add_argument("--keep-last-attempt",
                            dest="keep_last",
                            default=True,
                            type=bool,
                            help="In case of failure, keep the resources "
                                 "allocated in the last try (Default: True, "
                                 "accepts boolean values).")

        parser.add_argument('uuid',
                            metavar="<deployment uuid>",
                            help="Deployment UUID to update.")
        parser.add_argument('filename',
                            metavar="<template file>",
                            help="TOSCA template file.")
        parser.add_argument('parameters',
                            metavar="<parameter>=<value>",
                            nargs="*",
                            action=KeyValueAction,
                            help="Input parameter for the deployment in the "
                                 "form <parameter>=<value>. Can be specified "
                                 "several times.")
        return parser

    def take_action(self, parsed_args):
        with open(parsed_args.filename, "r") as f:
            d = self.app.client.deployments.update(
                uuid=parsed_args.uuid,
                template=f.read(),
                callback_url=parsed_args.callback,
                max_providers_retry=parsed_args.max_retries,
                keep_last_attemp=parsed_args.keep_last,
                parameters=parsed_args.parameters
            )
        return self.dict2columns(d.to_dict())

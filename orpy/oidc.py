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

import json
import socket

from orpy import exceptions
from orpy import utils


class OpenIDConnectAgent(object):
    """Communicate with an OpenID Connect agent."""

    def __init__(self, account, socket_path=None, validity=60):
        """Initialize OpenID Connect Agent connection.

        :param str account: Account name to use
        :param str socket_path: Path to the oidc-agent UNIX socket
        :param int validity: Minimum validity (minutes) for the token
        """
        self.account = account
        self.validity = validity

        if socket_path is None:
            socket_path = utils.env("OIDC_SOCK")

        self.socket_path = socket_path

    def get_token(self):
        """Communicate with the oidc agent and get an access token.

        :returns: A dictionary containing the access token
        :rtype: dict
        """
        message = {
            "request": "access_token",
            "account": self.account,
            "min_valid_period": self.validity,
            "application_hint": "orpy",
        }
        try:
            self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._sock.connect(self.socket_path)
            self._sock.sendall(json.dumps(message).encode())

            data = ""
            while True:
                recv = self._sock.recv(16).decode()
                if recv:
                    data += recv
                else:
                    break
        except socket.error as err:
            raise exceptions.AuthExceptiob(err="Cannot communicate with the "
                                               "oidc-agent: %s" % err)
        finally:
            self._sock.close()

        token = json.loads(data)
        if token.get("status") == "failure":
            raise exceptions.AuthException(err=token.get("error"))
        return token

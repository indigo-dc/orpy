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

import copy


class BaseObject(object):
    """Base class for all objects that represents orchestrator resoruces."""

    def __init__(self, info):
        """Initalize the object.

        :param dict info: A dictionary object containing the object's
                          information
        """
        self._info = {}
        self._add_details(info)
        self.uuid = info.get("uuid", None)

    def __repr__(self):
        reprkeys = sorted(k
                          for k in self.__dict__.keys()
                          if k[0] != '_')
        info = ", ".join("%s=%s" % (k, getattr(self, k)) for k in reprkeys)
        return "<%s %s>" % (self.__class__.__name__, info)

    def _add_details(self, info):
        for (k, v) in info.items():
            try:
                setattr(self, k, v)
                self._info[k] = v
            except AttributeError:
                # In this case we already defined the attribute on the class
                pass

    def __getattr__(self, k):
        if k not in self.__dict__:
            raise AttributeError(k)
        else:
            return self.__dict__[k]

    def __eq__(self, other):
        if not isinstance(other, BaseObject):
            return NotImplemented
        # two resources of different types are not equal
        if not isinstance(other, self.__class__):
            return False
        if hasattr(self, 'id') and hasattr(other, 'id'):
            return self.id == other.id
        return self._info == other._info

    def __ne__(self, other):
        # Using not of '==' implementation because the not of
        # __eq__, when it returns NotImplemented, is returning False.
        return not self == other

    def set_info(self, key, value):
        """Set an objects information with key, value.

        :param key: the element to set
        :param value: the value for the element
        """
        self._info[key] = value

    def to_dict(self):
        """Translate the object into a dictionary.

        :return: A dictionary contaning the object representation
        :rtype: dict
        """
        return copy.deepcopy(self._info)

    def get(self, k, default=None):
        try:
            return self.__getattr__(k)
        except AttributeError:
            return default


class Deployment(BaseObject):
    """Object that represents a deployment."""
    pass


class Resource(BaseObject):
    """Object that represents a Resource."""
    pass


class TOSCATemplate(BaseObject):
    """Object that repesents a TOSCA template."""
    pass


class OrchestratorInfo(BaseObject):
    """Object that represents the Orchestrtor information."""
    pass


class OrchestratorConfiguration(BaseObject):
    """Object that represents the Orchestrtor information."""
    pass

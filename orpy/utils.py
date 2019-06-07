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

import os


def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars
    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.
    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
    return kwargs.get('default', '')


def get_item_properties(item, fields, mixed_case_fields=None):
    """Return a tuple containing the item properties.
    :param item: a single item resource (e.g. Server, Project, etc)
    :param fields: tuple of strings with the desired field names
    :param mixed_case_fields: tuple of field names to preserve case
    """
    if mixed_case_fields is None:
        mixed_case_fields = []

    row = []

    for field in fields:
        if field in mixed_case_fields:
            field_name = field.replace(' ', '')
        else:
            field_name = field.lower().replace(' ', '')

        # FIXME(aloga): we need to move to objects, therefore
        # we need to adapt this asap
#        data = getattr(item, field_name, '')
        data = item.get(field_name, '')

        row.append(data)
    return tuple(row)

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

import six


class ClientException(Exception):
    message = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if not message:
            try:
                message = self.message % kwargs
            except Exception:
                exc_info = sys.exc_info()
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                print('Exception in string format operation')
                for name, value in kwargs.iteritems():
                    print("%s: %s" % (name, value))
                six.reraise(exc_info[0], exc_info[1], exc_info[2])

        message = "ERROR: " + message
        super(ClientException, self).__init__(message)


class AuthException(ClientException):
    message = ("An exception has happened while obtaining an access token"
               " (err: %(err)s)")


class InvalidUsage(ClientException):
    message = "Invalid client usage"


class InvalidUrl(ClientException):
    message = "URL provided is not a valid orchestrator (%(url)s)"


class RetryAfterException(ClientException):
    """Base class for ClientExceptions that use Retry-After header."""
    def __init__(self, *args, **kwargs):
        try:
            self.retry_after = int(kwargs.pop('retry_after'))
        except (KeyError, ValueError):
            self.retry_after = 0

        super(RetryAfterException, self).__init__(*args, **kwargs)


class BadRequest(ClientException):
    """HTTP 400 - Bad request.

    You sent some malformed data.
    """
    http_status = 400
    message = "Bad request"


class Unauthorized(ClientException):
    """HTTP 401 - Unauthorized.

    Bad credentials.
    """
    http_status = 401
    message = "Unauthorized"


class Forbidden(ClientException):
    """HTTP 403 - Forbidden.

    Your credentials don't give you access to this resource.
    """
    http_status = 403
    message = "Forbidden"


class NotFound(ClientException):
    """HTTP 404 - Not found."""
    http_status = 404
    message = "Not found"


class MethodNotAllowed(ClientException):
    """HTTP 405 - Method Not Allowed."""
    http_status = 405
    message = "Method Not Allowed"


class NotAcceptable(ClientException):
    """HTTP 406 - Not Acceptable."""
    http_status = 406
    message = "Not Acceptable"


class Conflict(ClientException):
    """HTTP 409 - Conflict."""
    http_status = 409
    message = "Conflict"


class OverLimit(RetryAfterException):
    """HTTP 413 - Over limit.

    You're over the API limits for this time period.
    """
    http_status = 413
    message = "Over limit"


class RateLimit(RetryAfterException):
    """HTTP 429 - Rate limit

    You've sent too many requests for this time period.
    """
    http_status = 429
    message = "Rate limit"


# NotImplemented is a python keyword.
class HTTPNotImplemented(ClientException):
    """HTTP 501 - Not Implemented.

    The server does not support this operation.
    """
    http_status = 501
    message = "Not Implemented"


# In Python 2.4 Exception is old-style and thus doesn't have a __subclasses__()
# so we can do this:
#     _code_map = dict((c.http_status, c)
#                      for c in ClientException.__subclasses__())
#
# Instead, we have to hardcode it:
_error_classes = [BadRequest, Unauthorized, Forbidden, NotFound,
                  MethodNotAllowed, NotAcceptable, Conflict, OverLimit,
                  RateLimit, HTTPNotImplemented]
_code_map = dict((c.http_status, c) for c in _error_classes)


def from_response(response, body, url, method=None):
    """Return an instance of ClientException or subclass based on a response.

    Usage::

        resp, body = requests.request(...)
        if resp.status_code != 200:
            raise exception_from_response(resp, rest.text)
    """
    cls = _code_map.get(response.status_code, ClientException)

    kwargs = {
        'code': response.status_code,
        'method': method,
        'url': url,
        'request_id': None,
    }

    if body:
        message = "n/a"
        details = "n/a"

        if hasattr(body, 'keys'):
            # NOTE(mriedem): WebOb<1.6.0 will return a nested dict structure
            # where the error keys to the message/details/code. WebOb>=1.6.0
            # returns just a response body as a single dict, not nested,
            # so we have to handle both cases (since we can't trust what we're
            # given with content_type: application/json either way.
            if 'message' in body:
                # WebOb 1.6.0 case
                message = body.get('message')
                details = body.get('details')
            else:
                # WebOb<1.6.0 where we assume there is a single error message
                # key to the body that has the message and details.
                error = body[list(body)[0]]
                message = error.get('message')
                details = error.get('details')

        kwargs['message'] = message
        kwargs['details'] = details

    return cls(**kwargs)

# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Record Resource Configuration."""

from flask_resources.errors import HTTPJSONException, create_errormap_handler
from flask_resources.parsers import HeadersParser, URLArgsParser
from flask_resources.resources import ResourceConfig
from flask_resources.serializers import JSONSerializer
from invenio_pidstore.errors import PIDDeletedError, PIDDoesNotExistError, \
    PIDRedirectedError, PIDUnregistered
from uritemplate import URITemplate

from ..services.errors import PermissionDeniedError, RevisionIdMismatchError
from .errors import create_pid_redirected_error_handler
from .record_args import RequestHeadersSchema, SearchURLArgsSchema
from .record_response import RecordResponse


class RecordResourceConfig(ResourceConfig):
    """Record resource config."""

    list_route = "/records"
    item_route = f"{list_route}/<pid_value>"

    links_config = {
        "record": {
            "self": URITemplate(f"{list_route}{{/pid_value}}"),
        },
        "search": {
            "self": URITemplate(f"{list_route}{{?params*}}"),
            "prev": URITemplate(f"{list_route}{{?params*}}"),
            "next": URITemplate(f"{list_route}{{?params*}}"),
        }
    }

    request_url_args_parser = {
        "search": URLArgsParser(SearchURLArgsSchema)
    }

    request_headers_parser = {
        "update": HeadersParser(RequestHeadersSchema, allow_unknown=False),
        "delete": HeadersParser(RequestHeadersSchema, allow_unknown=False)
    }

    response_handlers = {
        "application/json": RecordResponse(JSONSerializer())
    }

    error_map = {
        RevisionIdMismatchError: create_errormap_handler(
            lambda e: HTTPJSONException(
                code=412,
                description=e.description,
            )
        ),
        PermissionDeniedError: create_errormap_handler(
            HTTPJSONException(
                code=403,
                description="Permission denied.",
            )
        ),
        PIDDeletedError: create_errormap_handler(
            HTTPJSONException(
                code=410,
                description="The record has been deleted.",
            )
        ),
        PIDDoesNotExistError: create_errormap_handler(
            HTTPJSONException(
                code=404,
                description="The pid does not exist.",
            )
        ),
        PIDUnregistered: create_errormap_handler(
            HTTPJSONException(
                code=404,
                description="The pid is not registered.",
            )
        ),
        PIDRedirectedError: create_pid_redirected_error_handler(),
    }

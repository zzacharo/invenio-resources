# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Resources is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Resources module to create REST APIs."""

from flask_babelex import gettext as _

from . import config
from .resources import RecordResource


class InvenioResources(object):
    """Invenio-Resources extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)

        record_bp = RecordResource().as_blueprint("record_resource")
        app.register_blueprint(record_bp)

        app.extensions["invenio-resources"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("RESOURCES_"):
                app.config.setdefault(k, getattr(config, k))

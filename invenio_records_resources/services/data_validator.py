# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Records-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Data validation API."""

from ..schemas import MetadataSchemaJSONV1


class DataValidatorSchema:

    def load(self, data, **kwargs):
        """Deserialize incoming data to internal represenation.

        :returns: The transformed data as a dict.
        """
        raise NotImplementedError()

    def dump(self, data, **kwargs):
        """Serialize internal representation.

        :returns: The serialized data as a dict.
        """
        raise NotImplementedError()


class DataValidator:
    """Data schema interface."""

    def __init__(self, schema):
        self.schema = schema

    def load(self, data, **kwargs):
        """Validate by dumping it on the marshmallow schema.

        :returns: The validated data as a dict.
        """
        return self.schema(**kwargs).load(data)

    def dump(self, data, **kwargs):
        """Validate by dumping it on the marshmallow schema.

        :returns: The validated data as a dict.
        """
        return self.schema(**kwargs).dump(data)


class MarshmallowDataValidator(DataValidator):
    """Data validator based on a Marshamllow schema."""

    def __init__(self):
        """Constructor."""
        super(MarshmallowDataValidator, self).__init__(
            schema=MetadataSchemaJSONV1
        )

# -*- coding: utf-8 -*-
"""
Testing class for the CastorField class.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
from castoredc_api.study.castor_objects.castor_field import CastorField


class TestCastorField:
    """Testing class for CastorField object unit tests."""

    def test_field_create(self):
        """Tests creation of a field."""
        field = CastorField(
            field_id="FAKE-SURVEY-FIELD-ID2",
            field_name="Survey Field 1a2",
            field_label="This is the second survey field",
            field_type="string",
            field_required="0",
            field_option_group=None,
            field_order="1",
        )
        assert type(field) is CastorField
        assert field.field_id == "FAKE-SURVEY-FIELD-ID2"

# -*- coding: utf-8 -*-
"""
Testing class for the CastorStep class.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
from castoredc_api.study.castor_objects.castor_field import CastorField
from castoredc_api.study.castor_objects.castor_step import CastorStep


class TestCastorStep:
    """Testing class for CastorStep object unit tests."""

    def test_step_create(self):
        """Tests creation of a step."""
        step = CastorStep("Report Step 2a", "FAKE-REPORT-STEP-ID3", "1")
        assert type(step) is CastorStep
        assert step.step_id == "FAKE-REPORT-STEP-ID3"

    def test_step_add_field(self):
        """Tests adding a field to a step."""
        step = CastorStep("Report Step 2a", "FAKE-REPORT-STEP-ID3", "1")
        field = CastorField(
            field_id="FAKE-REPORT-FIELD-ID7",
            field_name="Report Field 2a4",
            field_label="This is the fourth report field",
            field_type="test",
            field_required="1",
            field_option_group="FAKE-OPTION-GROUP-ID5",
            field_order="1",
        )
        step.add_field(field)
        assert len(step.fields_on_id) == 1
        assert step.fields_on_id["FAKE-REPORT-FIELD-ID7"] == field
        assert field.step == step

    def test_step_get_all_fields(self, steps_with_fields):
        """Tests getting all fields linked to a step."""
        step = steps_with_fields[0]
        fields = step.get_all_fields()
        assert len(fields) == 3
        for field in fields:
            assert type(field) is CastorField

    def test_step_get_single_field(self, steps_with_fields):
        """Tests getting a single field by id."""
        step = steps_with_fields[0]
        field = step.get_single_field("FAKE-SURVEY-FIELD-ID3")
        assert type(field) is CastorField
        assert field.field_id == "FAKE-SURVEY-FIELD-ID3"
        assert field.field_name == "Survey Field 1a3"

    def test_step_get_single_field_on_name(self, steps_with_fields):
        """Tests getting a single field by name."""
        step = steps_with_fields[0]
        field = step.get_single_field("Survey Field 1a3")
        assert type(field) is CastorField
        assert field.field_id == "FAKE-SURVEY-FIELD-ID3"
        assert field.field_name == "Survey Field 1a3"

    def test_step_get_single_field_fail(self, steps_with_fields):
        """Tests failing to get a single field by id."""
        step = steps_with_fields[0]
        field = step.get_single_field("FAKE-SURVEY-FIELD-ID4")
        assert field is None

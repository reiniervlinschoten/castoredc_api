# -*- coding: utf-8 -*-
"""
Testing class for the CastorForm class.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
from castoredc_api.study.castor_objects.castor_field import CastorField
from castoredc_api.study.castor_objects.castor_form import CastorForm
from castoredc_api.study.castor_objects.castor_step import CastorStep


class TestCastorForm:
    """Testing class for CastorForm object unit tests."""

    def test_form_create(self):
        """Tests creation of a form."""
        form = CastorForm("Fake Survey", "FAKE-SURVEY-ID1", "Survey", "1")
        assert type(form) is CastorForm
        assert form.form_id == "FAKE-SURVEY-ID1"

    def test_form_add_step(self):
        """Tests adding a step to a form."""
        form = CastorForm("Fake Survey", "FAKE-SURVEY-ID1", "Survey", "1")
        step = CastorStep("Survey Step 1a", "FAKE-SURVEY-STEP-ID1", "1")
        form.add_step(step)
        assert len(form.steps_on_id) == 1
        assert form.steps_on_id["FAKE-SURVEY-STEP-ID1"] == step
        assert step.form == form

    def test_form_get_all_steps(self, forms_with_steps):
        """Tests getting all steps linked to a form."""
        form = forms_with_steps[0]
        steps = form.get_all_steps()
        assert len(steps) == 3
        for step in steps:
            assert type(step) is CastorStep

    def test_form_get_single_step(self, forms_with_steps):
        """Tests getting a single step by id."""
        form = forms_with_steps[0]
        step = form.get_single_step("FAKE-SURVEY-STEP-ID2")
        assert type(step) is CastorStep
        assert step.step_id == "FAKE-SURVEY-STEP-ID2"
        assert step.step_name == "Survey Step 1b"

    def test_form_get_single_step_name(self, forms_with_steps):
        """Tests getting a single step by name."""
        form = forms_with_steps[0]
        step = form.get_single_step("Survey Step 1b")
        assert type(step) is CastorStep
        assert step.step_id == "FAKE-SURVEY-STEP-ID2"
        assert step.step_name == "Survey Step 1b"

    def test_form_get_single_step_fail(self, forms_with_steps):
        """Tests failing to get a single step by id."""
        form = forms_with_steps[0]
        step = form.get_single_step("FAKE-SURVEY-STEP-ID4")
        assert step is None

    def test_form_get_all_fields(self, complete_study):
        """Tests getting all fields from a form."""
        form = complete_study.forms_on_id["FAKE-SURVEY-ID1"]
        fields = form.get_all_fields()
        assert len(fields) == 6
        for field in fields:
            assert type(field) is CastorField

    def test_form_get_single_field(self, complete_study):
        """Tests getting a single field by id."""
        form = complete_study.forms_on_id["FAKE-SURVEY-ID1"]
        field = form.get_single_field("FAKE-SURVEY-FIELD-ID3")
        assert type(field) is CastorField
        assert field.field_id == "FAKE-SURVEY-FIELD-ID3"
        assert field.field_name == "Survey Field 1a3"

    def test_form_get_single_field_name(self, complete_study):
        """Tests getting a single field by name."""
        form = complete_study.forms_on_id["FAKE-SURVEY-ID1"]
        field = form.get_single_field("Survey Field 1a3")
        assert type(field) is CastorField
        assert field.field_id == "FAKE-SURVEY-FIELD-ID3"
        assert field.field_name == "Survey Field 1a3"

    def test_form_get_single_field_fail(self, complete_study):
        """Tests failing to get a single field by id."""
        form = complete_study.forms_on_id["FAKE-SURVEY-ID1"]
        field = form.get_single_field("FAKE-SURVEY-FIELD-ID7")
        assert field is None

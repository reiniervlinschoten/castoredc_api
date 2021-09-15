# -*- coding: utf-8 -*-
"""
Testing class for the CastorRecord class.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
from castoredc_api.study.castor_objects.castor_record import CastorRecord
from castoredc_api.study.castor_objects.castor_report_form_instance import (
    CastorReportFormInstance,
)
from castoredc_api.study.castor_objects.castor_study_form_instance import (
    CastorStudyFormInstance,
)
from castoredc_api.study.castor_objects.castor_survey_form_instance import (
    CastorSurveyFormInstance,
)


class TestCastorRecord:
    """Testing class for CastorRecord object unit tests."""

    def test_record_create(self):
        """Tests creation of a record point."""
        record = CastorRecord("110001")
        assert type(record) is CastorRecord
        assert record.record_id == "110001"
        assert len(record.form_instances_ids) == 0

    def test_record_add_form_instance(self, complete_study):
        """Tests adding a form instance to a record."""
        record = CastorRecord("110001")
        complete_study.add_record(record)
        form_instance = CastorSurveyFormInstance(
            "FAKE-SURVEY-INSTANCE-ID1", "Fake Survey", complete_study
        )
        record.add_form_instance(form_instance)
        assert len(record.form_instances_ids) == 1
        assert record.form_instances_ids["FAKE-SURVEY-INSTANCE-ID1"] == form_instance
        assert form_instance.record == record

    def test_record_get_all_form_instances(self, records_with_form_instances):
        """Tests getting all form instances linked to a record."""
        record = records_with_form_instances[0]
        forms = record.get_all_form_instances()
        assert len(forms) == 4
        for form in forms:
            assert type(form) in [
                CastorSurveyFormInstance,
                CastorReportFormInstance,
                CastorStudyFormInstance,
            ]

    def test_form_get_single_form_instance(self, records_with_form_instances):
        """Tests getting a single form instance linked to a record"""
        record = records_with_form_instances[0]
        form = record.get_single_form_instance_on_id("FAKE-SURVEY-INSTANCE-ID1")
        assert type(form) is CastorSurveyFormInstance
        assert form.instance_id == "FAKE-SURVEY-INSTANCE-ID1"
        assert form.name_of_form == "Fake Survey"

    def test_form_get_single_form_instance_fail(self, records_with_form_instances):
        """Tests failing to get a single form instance by id."""
        record = records_with_form_instances[0]
        form = record.get_single_form_instance_on_id("FAKE-SURVEY-INSTANCE-ID3")
        assert form is None

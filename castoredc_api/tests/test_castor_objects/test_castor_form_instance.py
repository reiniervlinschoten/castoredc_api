# -*- coding: utf-8 -*-
"""
Testing class for the CastorFormInstance class.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest

from castoredc_api.study.castor_objects.castor_data_point import CastorDataPoint
from castoredc_api.study.castor_objects.castor_report_form_instance import (
    CastorReportFormInstance,
)
from castoredc_api.study.castor_objects.castor_study_form_instance import (
    CastorStudyFormInstance,
)
from castoredc_api.study.castor_objects.castor_survey_form_instance import (
    CastorSurveyFormInstance,
)


class TestCastorFormInstance:
    """Testing class for CastorFormInstance object unit tests."""

    def test_survey_form_instance_create(self, complete_study):
        """Tests creation of a Survey form instance."""
        form_instance = CastorSurveyFormInstance(
            "FAKE-SURVEY-INSTANCE-ID3", "Fake Survey", complete_study
        )
        assert type(form_instance) is CastorSurveyFormInstance
        assert form_instance.instance_id == "FAKE-SURVEY-INSTANCE-ID3"
        assert form_instance.instance_type == "Survey"
        assert form_instance.name_of_form == "Fake Survey"
        assert form_instance.instance_of.form_id == "FAKE-SURVEY-ID1"

    def test_report_form_instance_create(self, complete_study):
        """Tests creation of a Report form instance."""
        form_instance = CastorReportFormInstance(
            "FAKE-REPORT-INSTANCE-ID2", "Report Name #90212", complete_study
        )
        assert type(form_instance) is CastorReportFormInstance
        assert form_instance.instance_id == "FAKE-REPORT-INSTANCE-ID2"
        assert form_instance.instance_type == "Report"
        assert form_instance.name_of_form == "Report Name #90212"
        assert form_instance.instance_of.form_id == "FAKE-REPORT-ID2"

    def test_study_form_instance_create(self, complete_study):
        """Tests creation of a Study form instance."""
        form_instance = CastorStudyFormInstance(
            "FAKE-STUDYIDFAKE-STUDYIDFAKE-STUDYID", "Baseline", complete_study
        )
        assert type(form_instance) is CastorStudyFormInstance
        assert form_instance.instance_id == "FAKE-STUDYIDFAKE-STUDYIDFAKE-STUDYID"
        assert form_instance.instance_type == "Study"
        assert form_instance.name_of_form == "Baseline"
        assert (
            form_instance.instance_of.form_id == "FAKE-STUDYIDFAKE-STUDYIDFAKE-STUDYID"
        )

    def test_survey_form_instance_create_fail(self, complete_study):
        """Tests creation of a Survey form instance."""
        with pytest.raises(KeyError) as e:
            CastorSurveyFormInstance(
                "FAKE-SURVEY-INSTANCE-ID60",
                "Maximum Fake Survey",
                complete_study,
            )
        assert str(e.value) == "'Maximum Fake Survey'"

    def test_report_form_instance_create_fail(self, complete_study):
        """Tests creation of a Report form instance."""
        with pytest.raises(KeyError) as e:
            CastorReportFormInstance(
                "FAKE-REPORT-INSTANCE-ID3",
                "Report Name #90212",
                complete_study,
            )
        assert str(e.value) == "'FAKE-REPORT-INSTANCE-ID3'"

    def test_form_instance_add_data_point(self, complete_study):
        """Tests adding a data point to a form instance.."""
        form_instance = CastorStudyFormInstance(
            "FAKE-STUDYIDFAKE-STUDYIDFAKE-STUDYID", "Baseline", complete_study
        )
        data_point = CastorDataPoint(
            "FAKE-STUDY-FIELD-ID3", "test", complete_study, "2021-01-15 13:39:47"
        )
        assert len(form_instance.data_points_on_id) == 0
        form_instance.add_data_point(data_point)
        assert len(form_instance.data_points_on_id) == 1
        assert form_instance.data_points_on_id["FAKE-STUDY-FIELD-ID3"] == data_point
        assert data_point.form_instance == form_instance

    def test_form_instances_get_all_data_points(self, instances_with_data_points):
        """Tests getting all data points linked to a form instance."""
        form_instance = instances_with_data_points[0]
        data_points = form_instance.get_all_data_points()
        assert len(data_points) == 3
        for data_point in data_points:
            assert type(data_point) is CastorDataPoint

    def test_form_get_single_data_point(self, instances_with_data_points):
        """Tests getting a single data point linked to a form_instance"""
        form_instance = instances_with_data_points[0]
        data_point = form_instance.get_single_data_point("FAKE-SURVEY-FIELD-ID2")
        assert type(data_point) is CastorDataPoint
        assert data_point.field_id == "FAKE-SURVEY-FIELD-ID2"
        assert data_point.raw_value == "test"

    def test_form_get_single_data_point_on_name(self, instances_with_data_points):
        """Tests getting a single data point linked to a form_instance"""
        form_instance = instances_with_data_points[0]
        data_point = form_instance.get_single_data_point("Survey Field 1a2")
        assert type(data_point) is CastorDataPoint
        assert data_point.field_id == "FAKE-SURVEY-FIELD-ID2"
        assert data_point.raw_value == "test"

    def test_form_get_single_form_instance_fail(self, instances_with_data_points):
        """Tests failing to get a single data point by id."""
        form_instance = instances_with_data_points[0]
        data_point = form_instance.get_single_data_point("FAKE-SURVEY-FIELD-ID6")
        assert data_point is None

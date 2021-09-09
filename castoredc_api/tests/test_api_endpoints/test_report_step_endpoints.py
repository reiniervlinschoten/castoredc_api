# -*- coding: utf-8 -*-
"""
Testing class for report step endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-step

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import report_step_model
from castoredc_api import CastorException


class TestReportStep:
    model_keys = report_step_model.keys()
    test_report_step = {
        "id": "111BA2F0-BC6B-47ED-9159-802BF7600BA6",
        "report_step_id": "111BA2F0-BC6B-47ED-9159-802BF7600BA6",
        "report_step_name": "Medication",
        "report_step_description": "This report form allows you to continuously collect medication data.",
        "report_step_number": 1,
        "_embedded": {
            "report": {
                "id": "89FF2394-0D41-4D4C-89FE-AA9AB287B31E",
                "report_id": "89FF2394-0D41-4D4C-89FE-AA9AB287B31E",
                "name": "Medication",
                "description": "Alle mogelijke repeated measures zijn hier te bewerken",
                "type": "repeated_measure",
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/report/89FF2394-0D41-4D4C-89FE-AA9AB287B31E"
                    }
                },
            }
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/report/89FF2394-0D41-4D4C-89FE-AA9AB287B31E/report-step/111BA2F0-BC6B-47ED-9159-802BF7600BA6"
            }
        },
    }

    @pytest.fixture(scope="class")
    def reports_with_steps(self, client):
        """Returns all the reports in the study with their corresponding steps."""
        reports_with_steps = {}
        all_reports = client.all_reports()
        for report in all_reports:
            steps = client.single_report_all_steps(report["id"])
            reports_with_steps[report["id"]] = steps
        return reports_with_steps

    def test_all_report_steps(self, reports_with_steps):
        """Tests whether the model of the steps is correct."""
        for report in reports_with_steps:
            assert len(reports_with_steps[report]) > 0
            for step in reports_with_steps[report]:
                # Tests if the right keys are in the model
                assert len(step) == len(self.model_keys)
                # Tests if the values belonging to the keys are of the right type
                api_keys = step.keys()
                for key in self.model_keys:
                    assert key in api_keys
                    assert type(step[key]) in report_step_model[key]

    def test_single_report_single_step_success(self, client, reports_with_steps):
        """Tests whether single_step returns the proper model."""
        # Get a step
        step = client.single_report_single_step(
            "89FF2394-0D41-4D4C-89FE-AA9AB287B31E",
            "111BA2F0-BC6B-47ED-9159-802BF7600BA6",
        )
        assert step == self.test_report_step

    def test_single_report_single_step_failure(self, client, reports_with_steps):
        """Tests whether the right error is thrown when a non-existent step is queried."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_report_single_step(
                "89FF2394-0D41-4D4C-89FE-AA9AB287B31E",
                "111BA2F0-BC6B-47ED-9159-802BF760FAKE",
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

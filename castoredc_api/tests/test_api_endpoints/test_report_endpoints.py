# -*- coding: utf-8 -*-
"""
Testing class for report endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import report_model
from castoredc_api import CastorException


class TestReport:
    model_keys = report_model.keys()

    test_report = {
        "id": "770DB401-6100-4CF5-A95F-3402B55EAC48",
        "report_id": "770DB401-6100-4CF5-A95F-3402B55EAC48",
        "name": "Comorbidities",
        "description": "",
        "type": "other",
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/report/770DB401-6100-4CF5-A95F-3402B55EAC48"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_reports(self, client):
        """Gets all reports from the study."""
        all_reports = client.all_reports()
        return all_reports

    def test_all_reports(self, all_reports, item_totals):
        """Tests if all reports are returned from the study."""
        assert len(all_reports) > 0, "No reports found in the study, is this right?"
        assert len(all_reports) == item_totals("/report")

    def test_all_reports_model(self, all_reports):
        """Tests if all_reports returns the right model."""
        for report in all_reports:
            api_keys = report.keys()
            # Tests if the model is the right length
            assert len(self.model_keys) == len(api_keys)
            # Tests if the keys and types of values are what they should be
            for key in self.model_keys:
                assert key in api_keys
                assert type(report[key]) in report_model[key]

    def test_all_reports_data(self, all_reports):
        """Tests the data of the reports returned by all_reports"""
        # Select a report
        report = next(
            (
                report
                for report in all_reports
                if report["report_id"] == "770DB401-6100-4CF5-A95F-3402B55EAC48"
            ),
            None,
        )
        # Check if the right data is returned.
        assert report == self.test_report

    def test_single_report_success(self, client):
        """Tests if single report returns the proper data."""
        report = client.single_report("770DB401-6100-4CF5-A95F-3402B55EAC48")
        assert report == self.test_report

    def test_single_report_failure(self, client):
        """Tests if single report returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_report("FAKEB401-6100-4CF5-A95F-3402B55EAC48")
        assert "404 Client Error: Not Found for url" in str(e.value)

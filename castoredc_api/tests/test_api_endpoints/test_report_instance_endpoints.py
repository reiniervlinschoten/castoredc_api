# -*- coding: utf-8 -*-
"""
Testing class for report-instance endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-instance

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import report_instance_model
from castoredc_api import CastorException


def create_report_instance(record_id, fake):
    custom_name = str(random.randint(10000000, 99999999))

    if fake:
        report_id = "FAKEB401-6100-4CF5-A95F-3402B55EAC48'"
    else:
        report_id = "770DB401-6100-4CF5-A95F-3402B55EAC48"

    return {
        "record_id": record_id,
        "report_id": report_id,
        "report_name_custom": custom_name,
    }


class TestReportInstance:
    model_keys = report_instance_model.keys()

    test_report_instance = {
        "id": "382AE5BD-E728-4575-B467-142EA83813DE",
        "name": "20412282",
        "status": "open",
        "parent_id": "",
        "parent_type": "",
        "record_id": "110002",
        "report_name": "Unscheduled visit",
        "created_on": "2019-10-14 16:58:12",
        "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "archived": False,
        "_embedded": {
            "report": {
                "id": "C4ADC387-9BFD-4171-A861-6B973699A6ED",
                "report_id": "C4ADC387-9BFD-4171-A861-6B973699A6ED",
                "name": "Unscheduled visit",
                "description": "Follow-up visit",
                "type": "unscheduled_phase",
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/report/C4ADC387-9BFD-4171-A861-6B973699A6ED"
                    }
                },
            }
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17"
                "-71F2BB12A2FD/report-instance/382AE5BD-E728-4575-B467-142EA83813DE"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_report_instances(self, client):
        """Returns all report instances in the study."""
        all_report_instances = client.all_report_instances()
        return all_report_instances

    def test_all_report_instances(self, all_report_instances, item_totals):
        """Tests if all report instances are returned."""
        assert (
            len(all_report_instances) > 0
        ), "No report instances found in the study, is this right?"
        assert len(all_report_instances) == item_totals("/report-instance")

    def test_all_report_instances_model(self, all_report_instances):
        """Tests the model returned by all_report_instances."""
        for report_instance in all_report_instances:
            api_keys = report_instance.keys()
            # Tests if the model is the right length
            assert len(self.model_keys) == len(api_keys)
            # Tests if the right keys and types of values are returned
            for key in self.model_keys:
                assert key in api_keys
                assert type(report_instance[key]) in report_instance_model[key]

    def test_single_report_instance_success(self, client):
        """Tests if single report_instance returns the proper data."""
        report_instance = client.single_report_instance(
            "382AE5BD-E728-4575-B467-142EA83813DE"
        )
        assert report_instance == self.test_report_instance

    def test_single_report_instance_fail(self, client):
        """Tests if single report_instance returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_report_instance("FAKEE5BD-E728-4575-B467-142EA83813DE")
        assert "400 Client Error: Bad Request for url:" in str(e.value)

    def test_all_report_instances_record_success(self, client):
        """Tests if the model that is returned if filtered on record is proper."""
        reports = client.all_report_instances_record("000001")
        for report in reports:
            report_keys = report.keys()
            # Tests if the length of the model is right
            assert len(self.model_keys) == len(report_keys)
            # Tests if they keys and types of values are right
            for key in self.model_keys:
                assert key in report_keys
                assert type(report[key]) in report_instance_model[key]

    def test_all_report_instances_record_fail(self, client):
        """Tests if a proper error is thrown when the wrong record is filtered on."""
        with pytest.raises(HTTPStatusError) as e:
            client.all_report_instances_record("FAKE01")
        assert "404 Client Error: Not Found for url:" in str(e.value)

    def test_single_report_instance_record_success(self, client):
        """Tests if the model of a single report after filtering on record is right"""
        report = client.single_report_instance_record(
            "000001", "31EB7B5F-7159-430B-A7E5-90A714D346B9"
        )
        report_keys = report.keys()
        # Tests if the length of the model is right
        assert len(self.model_keys) == len(report_keys)
        # Tests if they keys and types of values are right
        for key in self.model_keys:
            assert key in report_keys
            assert type(report[key]) in report_instance_model[key]

    def test_single_report_instance_record_fail(self, client):
        """Tests if filtering on a non-existent report throws an error for a filtered record."""
        with pytest.raises(HTTPStatusError) as e:
            # Query a report belonging to a different record.
            client.single_report_instance_record(
                "000001", "61870790-F83E-4B1B-AF09-6F2CBA4632EA"
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_create_report_instance_record_success(self, client):
        """Tests creating a report for a record."""
        # Get baseline
        record_reports = client.all_report_instances_record("000003")
        amount_reports = len(record_reports)

        # Create a record
        report_instance = create_report_instance("000003", fake=False)
        created = client.create_report_instance_record(**report_instance)

        # Tests if creating was successful
        assert created["name"] == report_instance["report_name_custom"]
        assert created["record_id"] == report_instance["record_id"]

        # Tests if it was added to the database
        record_reports = client.all_report_instances_record("000003")
        new_amount = len(record_reports)
        assert amount_reports + 1 == new_amount

    def test_create_report_instance_record_fail(self, client):
        """Tests if a proper error is thrown when report creation failed."""
        # Get baseline
        record_reports = client.all_report_instances_record("000004")
        amount_reports = len(record_reports)
        report_instance = create_report_instance("000004", fake=True)

        # Create the record
        with pytest.raises(HTTPStatusError) as e:
            client.create_report_instance_record(**report_instance)
        assert "400 Client Error: Bad Request for url:" in str(e.value)

        # Test that nothing changed
        record_reports = client.all_report_instances_record("000004")
        new_amount = len(record_reports)
        assert amount_reports == new_amount

    def test_create_multiple_report_instances_record_success(self, client):
        """Tests creating multiple report instances at once."""
        # Get baseline
        record_reports = client.all_report_instances_record("000005")
        amount_reports = len(record_reports)

        # Create reports
        reports = []
        for i in range(0, 3):
            report_instance = create_report_instance("000005", fake=False)
            reports.append(report_instance)

        # Create reports
        created = client.create_multiple_report_instances_record("000005", reports)

        # Assert creation was successful
        assert created["total_success"] == 3
        assert created["total_failed"] == 0

        # Assert changes in the database
        record_reports = client.all_report_instances_record("000005")
        new_amount = len(record_reports)
        assert amount_reports + 3 == new_amount

    def test_create_multiple_report_instances_record_fail(self, client):
        """Tests multiple creation doesn't throw an error, but gives a warning from the database."""
        # Get baseline
        record_reports = client.all_report_instances_record("000006")
        amount_reports = len(record_reports)

        # Create reports
        reports = []
        for i in range(0, 3):
            report_instance = create_report_instance("000006", fake=True)
            reports.append(report_instance)
        created = client.create_multiple_report_instances_record("000006", reports)

        # Assert creation has failed
        assert created["total_success"] == 0
        assert created["total_failed"] == 3

        # Assert database has not changed
        record_reports = client.all_report_instances_record("000006")
        new_amount = len(record_reports)
        assert amount_reports == new_amount

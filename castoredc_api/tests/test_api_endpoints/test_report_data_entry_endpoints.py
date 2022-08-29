# -*- coding: utf-8 -*-
"""
Testing class for report-data-entry endpoint of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-data-entry

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import (
    report_data_point_extended_model,
    data_options,
)
from castoredc_api import CastorException
from castoredc_api.tests.test_api_endpoints.helpers_api_endpoints import allowed_value


class TestReportDataEntry:
    model_keys = report_data_point_extended_model.keys()
    data_options = data_options
    test_field = {
        "record_id": "000004",
        "field_variable_name": "med_units",
        "field_id": "AFD46D4F-5C17-4B9B-BE19-8A5A702601C1",
        "report_instance_id": "2711B1EF-6118-4EBD-9858-47E4830C4EC5",
        "value": "1",
        "updated_on": "2020-08-14 12:55:46",
        "_embedded": {
            "record": {
                "id": "000004",
                "record_id": "000004",
                "record_status": None,
                "ccr_patient_id": "",
                "last_opened_step": "FFF23B2C-AEE6-4304-9CC4-9C7C431D5387",
                "locked": False,
                "progress": 17,
                "status": "open",
                "archived": False,
                "archived_reason": None,
                "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
                "created_on": {
                    "date": "2019-10-28 10:54:07.000000",
                    "timezone_type": 3,
                    "timezone": "Europe/Amsterdam",
                },
                "updated_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
                "updated_on": {
                    "date": "2020-08-14 13:20:27.000000",
                    "timezone_type": 3,
                    "timezone": "Europe/Amsterdam",
                },
                "randomized_id": None,
                "randomized_on": None,
                "randomization_group": None,
                "randomization_group_name": None,
                "_embedded": {
                    "institute": {
                        "id": "1CFF5802-0B07-471F-B97E-B5166332F2C5",
                        "institute_id": "1CFF5802-0B07-471F-B97E-B5166332F2C5",
                        "name": "Test Institute",
                        "abbreviation": "TES",
                        "date_format": "d-m-Y",
                        "code": "TES",
                        "order": 0,
                        "deleted": False,
                        "country_id": 169,
                        "_links": {
                            "self": {
                                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/institute/1CFF5802-0B07-471F-B97E-B5166332F2C5"
                            }
                        },
                    }
                },
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/record/000004"
                    }
                },
            },
            "field": {
                "id": "AFD46D4F-5C17-4B9B-BE19-8A5A702601C1",
                "parent_id": "111BA2F0-BC6B-47ED-9159-802BF7600BA6",
                "field_id": "AFD46D4F-5C17-4B9B-BE19-8A5A702601C1",
                "field_image": "",
                "field_number": 5,
                "field_label": "Units",
                "field_variable_name": "med_units",
                "field_type": "dropdown",
                "field_required": 1,
                "field_hidden": 0,
                "field_info": "",
                "field_units": "",
                "field_min": None,
                "field_min_label": "",
                "field_max": None,
                "field_max_label": "",
                "field_summary_template": "",
                "field_slider_step": None,
                "field_slider_step_value": None,
                "report_id": "",
                "field_length": None,
                "additional_config": "",
                "exclude_on_data_export": False,
                "field_enforce_decimals": None,
                "option_group": None,
                "metadata_points": [],
                "validations": [],
                "dependency_parents": [],
                "dependency_children": [],
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/field/AFD46D4F-5C17-4B9B-BE19-8A5A702601C1"
                    }
                },
            },
            "report_instance": {
                "id": "2711B1EF-6118-4EBD-9858-47E4830C4EC5",
                "name": "55437058",
                "status": "open",
                "parent_id": "",
                "parent_type": "",
                "record_id": "000004",
                "report_name": "Medication",
                "archived": False,
                "created_on": "2020-08-14 09:13:54",
                "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
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
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/record/000004/report-instance/2711B1EF-6118-4EBD-9858-47E4830C4EC5"
                    }
                },
            },
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/record/000004/data-point/report/2711B1EF-6118-4EBD-9858-47E4830C4EC5/AFD46D4F-5C17-4B9B-BE19-8A5A702601C1"
            }
        },
    }

    def test_single_report_instance_all_fields_record_success(self, client):
        """Tests returning a single report instance"""
        report = client.single_report_instance_all_fields_record(
            "000004", "2711B1EF-6118-4EBD-9858-47E4830C4EC5"
        )

        for field in report:
            field_keys = field.keys()
            assert len(field_keys) == len(self.model_keys)
            for key in field_keys:
                assert key in self.model_keys
                assert type(field[key]) in report_data_point_extended_model[key]

    def test_single_report_instance_all_fields_record_fail(self, client):
        """Tests failing to return a single report instance"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_report_instance_all_fields_record(
                "00FAKE", "2711B1EF-6118-4EBD-9858-47E4830C4EC5"
            )
        assert e.value.response.status_code == 404

    def test_single_report_instance_single_field_record_success(self, client):
        """Tests returning a single field from a report instance"""
        field = client.single_report_instance_single_field_record(
            "000004",
            "2711B1EF-6118-4EBD-9858-47E4830C4EC5",
            "AFD46D4F-5C17-4B9B-BE19-8A5A702601C1",
        )
        assert field == self.test_field

    def test_single_report_instance_single_field_record_fail(self, client):
        """Tests failing to return a single field from a report instance"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_report_instance_single_field_record(
                "000004",
                "2711B1EF-6118-4EBD-9858-47E4830C4EC5",
                "AFD46D4F-5C17-4B9B-BE19-8A5A7026FAKE",
            )
        assert e.value.response.status_code == 404

    def test_update_report_instance_single_field_record_success(self, write_client):
        """Tests updating a single field from a report instance"""
        # Get all filled in report data points
        field = "E08E1580-5E85-49BE-A547-89C2E15385A5"
        post_value = allowed_value(write_client, field)

        # Update the field
        change_reason = "Testing API"
        write_client.update_report_instance_single_field_record(
            "110001",
            "2CDE922C-6333-4D18-B8DC-912004D30FB5",
            field,
            change_reason,
            post_value,
        )

        # Check if changing worked
        new_value = write_client.single_report_instance_single_field_record(
            "110001", "2CDE922C-6333-4D18-B8DC-912004D30FB5", field
        )
        assert new_value["value"] == str(post_value)

    def test_update_report_instance_single_field_record_fail(self, write_client):
        """Tests failing to update a single field from a report instance"""
        # Get all filled in report data points
        field = "E08E1580-5E85-49BE-A547-89C2E15385A5"
        post_value = allowed_value(write_client, field)
        old_value = write_client.single_report_instance_single_field_record(
            "110001", "2CDE922C-6333-4D18-B8DC-912004D30FB5", field
        )

        # Update the field
        change_reason = "Testing API"

        with pytest.raises(HTTPStatusError) as e:
            write_client.update_report_instance_single_field_record(
                "110001",
                "2CDE922C-6333-4D18-B8DC-912004D30FB5",
                field + "FAKE",
                change_reason,
                post_value,
            )
        assert e.value.response.status_code == 404

        # Check if changing actually failed
        new_value = write_client.single_report_instance_single_field_record(
            "110001", "2CDE922C-6333-4D18-B8DC-912004D30FB5", field
        )
        assert new_value["value"] == old_value["value"]

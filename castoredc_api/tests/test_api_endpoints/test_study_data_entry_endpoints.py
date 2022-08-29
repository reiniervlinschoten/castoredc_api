# -*- coding: utf-8 -*-
"""
Testing class for report-data-entry endpoint of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/report-data-entry

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api import CastorException
from castoredc_api.tests.test_api_endpoints.data_models import (
    study_data_point_extended_model,
)
from castoredc_api.tests.test_api_endpoints.helpers_api_endpoints import allowed_value


class TestStudyDataEntry:
    model_keys = study_data_point_extended_model.keys()
    test_field = {
        "record_id": "000004",
        "field_variable_name": "ic_versions",
        "field_id": "28D1A17B-51C3-4BDC-A604-7B2F6D5D5924",
        "value": "1",
        "updated_on": "2019-11-04 15:47:38",
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
                "id": "28D1A17B-51C3-4BDC-A604-7B2F6D5D5924",
                "parent_id": "FFF23B2C-AEE6-4304-9CC4-9C7C431D5387",
                "field_id": "28D1A17B-51C3-4BDC-A604-7B2F6D5D5924",
                "field_image": "",
                "field_number": 3,
                "field_label": "Consent forms (CFs) reviewed:",
                "field_variable_name": "ic_versions",
                "field_type": "checkbox",
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
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/field/28D1A17B-51C3-4BDC-A604-7B2F6D5D5924"
                    }
                },
            },
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/record/000004/data-point/study/28D1A17B-51C3-4BDC-A604-7B2F6D5D5924"
            }
        },
    }

    def test_all_study_data_record_success(self, client):
        """Test returning all study_data_points for a record"""
        study_data = client.all_study_fields_record("000001")
        for field in study_data:
            field_keys = field.keys()
            assert len(field_keys) == len(self.model_keys)
            for key in field_keys:
                assert key in self.model_keys
                assert type(field[key]) in study_data_point_extended_model[key]

    def test_all_study_data_record_fail(self, client):
        """Test failing to return all study_data_points for a record"""
        with pytest.raises(HTTPStatusError) as e:
            client.all_study_fields_record("00FAKE")
        assert e.value.response.status_code == 404

    def test_single_study_data_point_record_success(self, client):
        """Tests returning a single study data point for a record"""
        study_data = client.single_study_field_record(
            "000004", "28D1A17B-51C3-4BDC-A604-7B2F6D5D5924"
        )
        assert study_data == self.test_field

    def test_single_study_data_point_record_fail(self, client):
        """Tests failing to return a single study data point for a record"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_study_field_record(
                "000004", "28D1A17B-51C3-4BDC-A604-7B2F6D5DFAKE"
            )
        assert e.value.response.status_code == 500

    def test_update_single_study_field_record_success(self, write_client):
        """Tests changing a single study field."""
        record = "110001"
        field = "4E6E5ECF-B195-416A-9813-4714141C1B93"
        post_value = allowed_value(write_client, field)

        # Update the field
        change_reason = "Testing API"
        write_client.update_single_study_field_record(
            record, field, change_reason, post_value
        )

        # Check if changing worked
        new_value = write_client.single_study_field_record(record, field)
        assert new_value["value"] == str(post_value)

    def test_update_single_study_field_record_fail(self, write_client):
        """Tests failing to change a single study field."""
        record = "110001"
        field = "4E6E5ECF-B195-416A-9813-4714141C1B93"
        post_value = allowed_value(write_client, field)
        old_value = write_client.single_study_field_record(record, field)

        # Update the field
        change_reason = "Testing API"

        with pytest.raises(HTTPStatusError) as e:
            write_client.update_single_study_field_record(
                record, "FAKE" + field + "FAKE", change_reason, post_value
            )

        assert e.value.response.status_code == 500

        new_value = write_client.single_study_field_record(record, field)
        assert new_value["value"] == old_value["value"]

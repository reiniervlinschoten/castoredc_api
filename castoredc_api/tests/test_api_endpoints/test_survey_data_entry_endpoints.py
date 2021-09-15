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
    survey_data_point_extended_model,
    data_options,
)
from castoredc_api.tests.test_api_endpoints.helpers_api_endpoints import allowed_value


class TestSurveyDataEntry:
    model_keys = survey_data_point_extended_model.keys()
    data_options = data_options

    test_field = {
        "record_id": "000005",
        "field_variable_name": "SF12_1",
        "field_id": "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
        "survey_instance_id": "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E",
        "value": "1",
        "updated_on": "2020-08-14 11:59:20",
        "_embedded": {
            "record": {
                "id": "000005",
                "record_id": "000005",
                "ccr_patient_id": "",
                "last_opened_step": "FFF23B2C-AEE6-4304-9CC4-9C7C431D5387",
                "progress": 7,
                "status": "open",
                "archived": False,
                "archived_reason": None,
                "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
                "created_on": {
                    "date": "2019-10-28 13:30:15.000000",
                    "timezone_type": 3,
                    "timezone": "Europe/Amsterdam",
                },
                "updated_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
                "updated_on": {
                    "date": "2020-08-19 14:09:04.000000",
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
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/record/000005"
                    }
                },
            },
            "field": {
                "id": "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
                "parent_id": "C19211FE-1C53-43F9-BC85-460DF1255153",
                "field_id": "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
                "field_number": 5,
                "field_label": "How would you rate your overall health?",
                "field_variable_name": "SF12_1",
                "field_type": "radio",
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
                "report_id": "",
                "field_length": None,
                "additional_config": "",
                "exclude_on_data_export": False,
                "option_group": None,
                "metadata_points": [],
                "validations": [],
                "dependency_parents": [],
                "dependency_children": [],
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/field/FC4FAA2D-08FD-41F7-B482-444B2B6D3116"
                    }
                },
            },
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/record/000005/data-point/survey/1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E/FC4FAA2D-08FD-41F7-B482-444B2B6D3116"
            }
        },
    }

    def test_single_survey_instance_all_fields_record_success(self, client):
        """Tests if single survey instance returns the right data."""
        survey = client.single_survey_instance_all_fields_record(
            "000005", "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E"
        )
        for field in survey:
            field_keys = field.keys()
            assert len(field_keys) == len(self.model_keys)
            for key in field_keys:
                assert key in self.model_keys
                assert type(field[key]) in survey_data_point_extended_model[key]

    def test_single_survey_instance_all_fields_record_fail(self, client):
        """Tests if failing to call a single survey instance throws an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_survey_instance_all_fields_record(
                "00FAKE", "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E"
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

    @pytest.mark.xfail(reason="Castor Database Error", strict=True)
    def test_single_survey_instance_single_field_record_success(self, client):
        """Tests if single survey field returns the proper data."""
        field = client.single_survey_instance_single_field_record(
            "000005",
            "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E",
            "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
        )
        assert field == self.test_field

    def test_single_survey_instance_single_field_record_fail_record(self, client):
        """Tests if calling a single survey field throws an error when failing"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_survey_instance_single_field_record(
                "00FAKE",
                "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E",
                "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_update_survey_instance_single_field_record_success(self, client):
        """Tests correctly changing a single survey field"""
        field = "FC4FAA2D-08FD-41F7-B482-444B2B6D3116"
        post_value = allowed_value(client, field)

        # Update the field
        change_reason = "Testing API"
        client.update_survey_instance_single_field_record(
            "000011",
            "5F420735-03B5-4736-9CCA-D3B02DA2BFF4",
            field,
            post_value,
            change_reason,
        )

        # Check if changing worked
        new_value = client.single_survey_instance_single_field_record(
            "000011", "5F420735-03B5-4736-9CCA-D3B02DA2BFF4", field
        )
        assert new_value["value"] == str(post_value)

    def test_update_survey_instance_single_field_record_fail(self, client):
        """Tests failing to change a single survey field"""
        field = "ED12B07E-EDA8-4D64-8268-BE751BD5DB36"
        post_value = allowed_value(client, field)
        old_value = client.single_survey_instance_single_field_record(
            "110002", "0FFD2C09-C5F2-4072-BDF1-736516C0D60A", field
        )

        # Update the field
        change_reason = "Testing API"

        with pytest.raises(HTTPStatusError) as e:
            client.update_survey_instance_single_field_record(
                "110002",
                "0FFD2C09-C5F2-4072-BDF1-736516C0D60A",
                field + "FAKE",
                post_value,
                change_reason,
            )
        assert "400 Client Error: Bad Request for url:" in str(e.value)

        # Check if changing failed
        new_value = client.single_survey_instance_single_field_record(
            "110002", "0FFD2C09-C5F2-4072-BDF1-736516C0D60A", field
        )
        assert new_value["value"] == old_value["value"]

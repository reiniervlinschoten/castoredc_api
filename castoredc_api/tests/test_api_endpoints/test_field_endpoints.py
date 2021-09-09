# -*- coding: utf-8 -*-
"""
Testing class for field endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import field_model
from castoredc_api import CastorException


class TestField:
    model_keys = field_model.keys()

    test_field = {
        "id": "07FAD531-6335-44FD-8C5B-A59FA396F12F",
        "parent_id": "62062F44-0314-4B76-9527-914717786A42",
        "field_id": "07FAD531-6335-44FD-8C5B-A59FA396F12F",
        "field_number": 2,
        "field_label": "Medication",
        "field_variable_name": None,
        "field_type": "repeated_measures",
        "field_required": 0,
        "field_hidden": 0,
        "field_info": "",
        "field_units": "",
        "field_min": None,
        "field_min_label": "",
        "field_max": None,
        "field_max_label": "",
        "field_summary_template": "",
        "field_slider_step": None,
        "report_id": "89FF2394-0D41-4D4C-89FE-AA9AB287B31E",
        "field_length": None,
        "additional_config": '{"showReportOfAllPhases":"0"}',
        "exclude_on_data_export": False,
        "option_group": None,
        "metadata_points": [],
        "validations": [],
        "dependency_parents": [],
        "dependency_children": [],
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/field/07FAD531-6335-44FD-8C5B-A59FA396F12F"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_fields(self, client):
        """Get all fields from the API."""
        all_fields = client.all_fields()
        return all_fields

    def test_all_fields(self, all_fields, item_totals):
        """Test if all fields are returned."""
        assert len(all_fields) > 0, "No fields found in the study, is this right?"
        assert len(all_fields) == item_totals("/field")

    def test_all_fields_model(self, all_fields):
        """Tests the model of the fields returned by all_fields"""
        # Loop through all fields
        for field in all_fields:
            api_keys = field.keys()
            # Tests if API and model have same number of keys
            assert len(self.model_keys) == len(api_keys)
            # Tests if the API and model keys and value types are equal
            for key in api_keys:
                assert key in self.model_keys
                assert type(field[key]) in field_model[key]

    def test_all_fields_data(self, all_fields):
        """Tests the data of the fields returned by all_fields"""
        # Select a field
        field = all_fields[4]
        # Check if the right data is returned.
        assert field == self.test_field

    def test_single_field_success(self, client):
        """Tests if single field returns the proper data."""
        field = client.single_field("07FAD531-6335-44FD-8C5B-A59FA396F12F")
        assert field == self.test_field

    def test_single_field_failure(self, client):
        """Tests if single field returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_field("FAKE5B4D-D362-4A54-9063-7D3CBAAC0F21")
        assert "404 Client Error: Not Found for url" in str(e.value)

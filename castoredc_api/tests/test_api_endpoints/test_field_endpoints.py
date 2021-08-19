# -*- coding: utf-8 -*-
"""
Testing class for field endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest

from castoredc_api.tests.test_api_endpoints.data_models import field_model
from castoredc_api import CastorException


class TestField:
    model_keys = field_model.keys()

    test_field = {
        "id": "0C895B4D-D362-4A54-9063-7D3CBAAC0F21",
        "parent_id": "52109C76-EB23-4BCD-95EC-10AC5CD912BF",
        "field_id": "0C895B4D-D362-4A54-9063-7D3CBAAC0F21",
        "field_number": 4,
        "field_label": "Height",
        "field_variable_name": "pat_height",
        "field_type": "numeric",
        "field_required": 1,
        "field_hidden": 0,
        "field_info": "",
        "field_units": "m",
        "field_min": 1.4,
        "field_min_label": "",
        "field_max": 2.5,
        "field_max_label": "",
        "field_summary_template": "",
        "field_slider_step": None,
        "report_id": "",
        "field_length": 5,
        "additional_config": "",
        "exclude_on_data_export": False,
        "option_group": None,
        "metadata_points": [],
        "validations": [],
        "dependency_parents": [],
        "dependency_children": [],
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/field/0C895B4D-D362-4A54-9063-7D3CBAAC0F21"
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
        field = client.single_field("0C895B4D-D362-4A54-9063-7D3CBAAC0F21")
        assert field == self.test_field

    def test_single_field_failure(self, client):
        """Tests if single field returns an error."""
        with pytest.raises(CastorException) as e:
            client.single_field("FAKE5B4D-D362-4A54-9063-7D3CBAAC0F21")
        assert str(e.value) == "404 Entity not found."

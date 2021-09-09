# -*- coding: utf-8 -*-
"""
Testing class for field-validation endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field-validation

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import field_val_model
from castoredc_api import CastorException


class TestFieldValidation:
    model_keys = field_val_model.keys()

    test_field_val = {
        "id": 7,
        "type": "inclusion_stop",
        "value": "1",
        "operator": "==",
        "text": "Previous trial participation is an exclusion criterion. You cannot proceed with data entry.",
        "field_id": "7E7868E1-946B-41EF-A96D-E3248251C6F1",
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/field-validation/7"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_field_vals(self, client):
        """Gets all field validations from the API"""
        all_field_vals = client.all_field_validations()
        return all_field_vals

    def test_all_field_vals(self, all_field_vals, item_totals):
        """Tests if the API returns all field validations"""
        assert len(all_field_vals) > 0
        assert len(all_field_vals) == item_totals("/field-validation")

    def test_all_field_vals_model(self, all_field_vals):
        """Tests the model of all field validations."""
        for validation in all_field_vals:
            api_keys = validation.keys()
            # Tests if the API returns the proper number of keys
            assert len(self.model_keys) == len(api_keys)
            # Tests if the API returns the proper type for every key in the model
            for key in self.model_keys:
                assert key in api_keys
                assert type(validation[key]) in field_val_model[key]

    def test_all_field_vals_data(self, all_field_vals):
        """Tests the data of the field_vals returned by all_field_vals"""
        # Select a field
        field_val = all_field_vals[3]
        # Check if the right data is returned.
        assert field_val == self.test_field_val

    def test_single_field_val_success(self, client):
        """Tests if single field val returns the proper data."""
        field_val = client.single_field_validation("7")
        assert field_val == self.test_field_val

    def test_single_field_val_failure(self, client):
        """Tests if single field_opt returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_field_validation("2")
        assert "404 Client Error: Not Found for url" in str(e.value)

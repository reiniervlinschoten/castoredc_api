# -*- coding: utf-8 -*-
"""
Testing class for field-optiongroup endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field-optiongroup

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import field_opt_model
from castoredc_api import CastorException


class TestFieldOptionGroup:
    model_keys = field_opt_model.keys()

    test_field_opt = {
        "id": "1A90F1BC-1329-43B5-B494-DFBB87C21E99",
        "name": "Severity",
        "description": "",
        "layout": False,
        "options": [
            {
                "id": "89D3D962-236D-41F0-AEAD-01653A6E9DC9",
                "name": "Mild",
                "value": "1",
                "groupOrder": 0,
            },
            {
                "id": "5808B803-3F3F-4E76-A5D5-1FB6F04C6E1D",
                "name": "Moderate",
                "value": "2",
                "groupOrder": 1,
            },
            {
                "id": "0E85C3B9-10A0-486A-A56D-404AF10FC2D7",
                "name": "Severe",
                "value": "3",
                "groupOrder": 2,
            },
            {
                "id": "7E2443AA-7920-4748-B4DD-8499D45282D7",
                "name": "Life-threatening",
                "value": "4",
                "groupOrder": 3,
            },
        ],
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/field-optiongroup/1A90F1BC-1329-43B5-B494-DFBB87C21E99"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_field_opts(self, client):
        """Gets all field optiongroups from the API."""
        all_field_opts = client.all_field_optiongroups()
        return all_field_opts

    def test_all_field_opts(self, all_field_opts, item_totals):
        """Tests if the API returns all fields in the study."""
        assert (
            len(all_field_opts) > 0
        ), "No field optiongroups found in the study, is this right?"
        assert len(all_field_opts) == item_totals("/field-optiongroup")

    def test_all_field_opts_model(self, all_field_opts):
        """Tests the model of the field optiongroups returned by all_field_opts"""
        for field in all_field_opts:
            api_keys = field.keys()
            # Tests if API and model have same number of keys
            assert len(self.model_keys) == len(api_keys)
            # Tests if the API and model keys and value types are equal
            for key in api_keys:
                assert key in self.model_keys
                assert type(field[key]) in field_opt_model[key]

    def test_all_field_opts_data(self, all_field_opts):
        """Tests the data of the field_opts returned by all_field_opts"""
        # Select a field
        field_opt = all_field_opts[3]
        # Check if the right data is returned.
        assert field_opt == self.test_field_opt

    def test_single_field_opts_success(self, client):
        """Tests if single field returns the proper data."""
        field_opt = client.single_field_optiongroup(
            "1A90F1BC-1329-43B5-B494-DFBB87C21E99"
        )
        assert field_opt == self.test_field_opt

    def test_single_field_opts_failure(self, client):
        """Tests if single field_opt returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_field_optiongroup("FAKEF1BC-1329-43B5-B494-DFBB87C21E99")
        assert "404 Client Error: Not Found for url" in str(e.value)

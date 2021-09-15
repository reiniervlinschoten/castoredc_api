# -*- coding: utf-8 -*-
"""
Testing class for metadatatype endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/metadatatype

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import metadata_type_model
from castoredc_api import CastorException


class TestMetadataType:
    model_keys = metadata_type_model.keys()

    test_metadata_type = {
        "id": 3,
        "name": "SNOMED",
        "description": "SNOMED Metadata",
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/metadatatype/3"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_metadata_types(self, client):
        """Gets all metadata types from the API."""
        all_metadata_types = client.all_metadata_types()
        return all_metadata_types

    def test_all_metadata_types(self, all_metadata_types, item_totals):
        """Tests if all metadata types are returned by the api"""
        assert (
            len(all_metadata_types) > 0
        ), "No metadata types found in the study, is this right?"
        assert len(all_metadata_types) == item_totals("/metadatatype")

    def test_all_metadata_types_model(self, all_metadata_types):
        """Tests the model returned by all metadata types."""
        for metadatatype in all_metadata_types:
            api_keys = metadatatype.keys()
            # Tests if the right keys are returned
            assert len(self.model_keys) == len(api_keys)
            # Tests if the values belonging to the keys have the right type
            for key in self.model_keys:
                assert key in api_keys
                assert type(metadatatype[key]) in metadata_type_model[key]

    def test_all_metadata_types_data(self, all_metadata_types):
        """Tests the data of the metadata_types returned by all_metadata_types"""
        # Select a metadata_type
        metadata_type = all_metadata_types[0]
        # Check if the right data is returned.
        assert metadata_type == self.test_metadata_type

    def test_single_metadata_type_success(self, client):
        """Tests if single metadata_type returns the proper data."""
        metadata_type = client.single_metadata_type("3")
        assert metadata_type == self.test_metadata_type

    def test_single_metadata_type_failure(self, client):
        """Tests if single metadata_type returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_metadata_type("2")
        assert "404 Client Error: Not Found for url" in str(e.value)

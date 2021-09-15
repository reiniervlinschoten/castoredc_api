# -*- coding: utf-8 -*-
"""
Testing class for metadata endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/metadata

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import metadata_model
from castoredc_api import CastorException


class TestMetadata:
    model_keys = metadata_model.keys()

    test_metadata = {
        "id": "7CFA5E29-02BB-4C90-AA02-5F27A300D99E",
        "metadata_type": {"id": 3, "name": "SNOMED", "description": "SNOMED Metadata"},
        "parent_id": None,
        "value": "271649006",
        "description": "Systolic Blood Pressure",
        "element_type": "Field",
        "element_id": "942A5086-88AD-44B4-A63C-85F945EAFCC7",
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/metadata/7CFA5E29-02BB-4C90-AA02-5F27A300D99E"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_metadata(self, client):
        """Get all metadata"""
        all_metadata = client.all_metadata()
        return all_metadata

    def test_all_metadata(self, all_metadata, item_totals):
        """Tests if all metadata from the database is returned."""
        assert (
            len(all_metadata) > 0
        ), "No metadata was found in the study, is this right?"
        assert len(all_metadata) == item_totals("/metadata")

    def test_all_metadata_model(self, all_metadata):
        """Tests the model returned by all_metadata."""
        for metadata in all_metadata:
            api_keys = metadata.keys()
            # Tests if the right keys are in the model
            assert len(self.model_keys) == len(api_keys)
            # Tests if the values belonging to the keys are of the right type
            for key in self.model_keys:
                assert key in api_keys
                assert type(metadata[key]) in metadata_model[key]

    def test_all_metadata_data(self, all_metadata):
        """Tests the data of the metadata returned by all_metadata"""
        # Select a metadata
        metadata = all_metadata[0]
        # Check if the right data is returned.
        assert metadata == self.test_metadata

    def test_single_metadata_success(self, client):
        """Tests if single metadata returns the proper data."""
        metadata = client.single_metadata("7CFA5E29-02BB-4C90-AA02-5F27A300D99E")
        assert metadata == self.test_metadata

    def test_single_metadata_failure(self, client):
        """Tests if single metadata returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_metadata("FAKE5E29-02BB-4C90-AA02-5F27A300D99E")
        assert "404 Client Error: Not Found for url" in str(e.value)

# -*- coding: utf-8 -*-
"""
Testing class for institute endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/institute

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import institute_model
from castoredc_api import CastorException


class TestInstitute:
    model_keys = institute_model.keys()

    test_institute = {
        "id": "47846A79-E02E-4545-9719-95B8DDED9108",
        "institute_id": "47846A79-E02E-4545-9719-95B8DDED9108",
        "name": "Franciscus Gasthuis",
        "abbreviation": "SFG",
        "code": None,
        "order": 11,
        "deleted": False,
        "country_id": 169,
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/institute/47846A79-E02E-4545-9719-95B8DDED9108"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_institutes(self, client):
        """Gets all institutes from the API"""
        all_institutes = client.all_institutes()
        return all_institutes

    def test_all_institutes(self, all_institutes, item_totals):
        """Tests if the proper number of institutes is returned in the API."""
        assert (
            len(all_institutes) > 0
        ), "No institutes found in the study, is this right?"
        assert len(all_institutes) == item_totals("/institute")

    def test_all_institutes_model(self, all_institutes):
        """Tests the model returned by all_institutes"""
        for institute in all_institutes:
            api_keys = institute.keys()
            # Tests if the same number of keys is in both models
            assert len(self.model_keys) == len(api_keys)
            # Tests if the right type of value is associated with every key
            for key in self.model_keys:
                assert key in api_keys
                assert type(institute[key]) in institute_model[key]

    def test_all_institutes_data(self, all_institutes):
        """Tests the data of the institutes returned by all_institutes"""
        # Select a institute
        institute = all_institutes[1]
        # Check if the right data is returned.
        assert institute == self.test_institute

    def test_single_institute_success(self, client):
        """Tests if single institute returns the proper data."""
        institute = client.single_institute("47846A79-E02E-4545-9719-95B8DDED9108")
        assert institute == self.test_institute

    def test_single_institute_failure(self, client):
        """Tests if single institute returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_institute("FAKE6A79-E02E-4545-9719-95B8DDED9108")
        assert "404 Client Error: Not Found for url" in str(e.value)

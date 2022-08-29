# -*- coding: utf-8 -*-
"""
Testing class for randomization endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/randomization

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import random

import pytest
from httpx import HTTPStatusError
from castoredc_api.tests.test_api_endpoints.data_models import randomization_model
from castoredc_api.tests.test_api_endpoints.test_record_endpoints import create_record


class TestRecord:
    model_keys = randomization_model.keys()

    test_randomization = {
        "randomized_id": "001",
        "randomization_group": "1",
        "randomization_group_name": "Control",
        "randomized_on": {
            "date": "2021-10-06 14:08:26.000000",
            "timezone_type": 3,
            "timezone": "Europe/Amsterdam",
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/record/000142/randomization"
            }
        },
    }

    def test_single_randomization_success(self, client):
        """Tests if single randomization returns the proper data."""
        randomization = client.single_randomization("000142")
        assert randomization == self.test_randomization

    def test_single_randomization_failure(self, client):
        """Tests if single randomization returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_randomization("FAKE42")
        assert e.value.response.status_code == 404

    def test_randomize_success(self, write_client):
        """Tests randomizing a new record."""
        record = {
            "institute_id": "EBCA14F3-56E9-4F7A-9AD6-DD6E5C41A632",
            "email": "totallyfake@fakeemail.com",
            "ccr_patient_id": None,
        }
        created = write_client.create_record(**record)
        new_record_id = created["id"]
        randomization = write_client.create_randomization(new_record_id)
        api_keys = randomization.keys()
        # Tests if the model length is the same
        assert len(self.model_keys) == len(api_keys)
        # Tests if the model keys and type of values are the same
        for key in self.model_keys:
            assert key in api_keys
            assert type(randomization[key]) in randomization_model[key]

    def test_randomize_fail(self, client):
        """Tests if randomizing a record properly errors."""
        with pytest.raises(HTTPStatusError) as e:
            client.create_randomization("FAKE42")
        assert e.value.response.status_code == 404

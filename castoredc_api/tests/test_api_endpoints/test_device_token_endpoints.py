# -*- coding: utf-8 -*-
"""
Testing class for device_token endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/record-device-token

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.test_record_endpoints import create_record


@pytest.mark.xfail(
    reason="Not possible to connect under right scope (record), see issue #42",
    strict=True,
)
class TestDeviceToken:
    def test_single_token_success(self, client):
        """Tests if single token returns the proper data."""
        token = client.single_token("000024")
        assert token["device_token"] == "OLD_API_TOKEN"

    def test_single_field_failure(self, client):
        """Tests if single token returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_token("FAKE24")
        assert e.value.response.status_code == 404

    def test_create_token_success(self, client):
        """Tests if creating a token works."""
        record = create_record(fake=False)
        created = client.create_record(**record)
        new_record_id = created["id"]
        token = client.create_token(new_record_id, "NEW-API-TOKEN")
        assert token["device_token"] == "NEW-API-TOKEN"

    def test_create_token_failure(self, client):
        """Tests if failing to update a token fails properly"""
        with pytest.raises(HTTPStatusError) as e:
            # Record already has a token
            client.create_token("000024", "NEW-API-TOKEN")
        assert e.value.response.status_code == 422

    def test_update_token_success(self, client):
        """Tests if updating a token works."""
        token = client.update_token("000025", "NEW-API-TOKEN")
        assert token["device_token"] == "NEW_API_TOKEN"
        # Reset old situation
        client.update_token("000025", "OLD-API-TOKEN")

    def test_update_token_failure(self, client):
        """Tests if failing to update a token fails properly"""
        with pytest.raises(HTTPStatusError) as e:
            client.update_token("FAKE24", "NEW-API-TOKEN")
        assert e.value.response.status_code == 404

    def test_delete_token_success(self, client):
        """Tests if deleting a token works."""
        record = create_record(fake=False)
        created = client.create_record(**record)
        new_record_id = created["id"]
        token = client.create_token(new_record_id, "NEW-API-TOKEN")
        assert token["device_token"] == "NEW-API-TOKEN"
        delete = client.delete_token(new_record_id)
        assert delete["device_token"] == ""
        token = client.single_token(new_record_id)
        assert token["device_token"] == ""

    def test_delete_token_failure(self, client):
        """Tests if failing to update a token fails properly"""
        with pytest.raises(HTTPStatusError) as e:
            client.delete_token("000024")
        assert e.value.response.status_code == 404

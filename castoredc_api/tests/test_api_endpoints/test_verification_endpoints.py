# -*- coding: utf-8 -*-
"""
Testing class for verification endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/verification

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError


class TestVerification:
    def test_basic_verifications(self, client):
        """Tests basic verification functionality"""
        verifications = client.verifications()
        assert verifications == self.verification_data

    def test_verification_filter_record(self, client):
        """Tests verification functionality filtering on record"""
        verifications = client.verifications(record_id="000001")
        assert verifications == self.empty_verification_data

    def test_verification_filter_dates(self, client):
        """Tests verification functionality filtering on date"""
        verifications = client.verifications(
            date_from="2021-10-12", date_to="2021-10-12"
        )
        assert verifications == self.empty_verification_data

    def test_verification_filter_fail(self, client):
        """Tests verification functionality fails correctly"""
        with pytest.raises(ValueError) as e:
            client.verifications(date_from="12-10-2021", date_to="12-10-2021")
        assert "does not match format" in str(e.value)

    verification_data = [
        {
            "id": 2,
            "record_id": "000024",
            "entity_type": "field",
            "entity_id": "BFB50DCE-0563-4963-BAB8-899EE2475961",
            "parent_id": "",
            "verified_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
            "verified_on": {
                "date": "2021-10-13 15:19:39.000000",
                "timezone_type": 3,
                "timezone": "Europe/Amsterdam",
            },
            "status": "active",
            "dropped_by": None,
            "dropped_on": None,
            "changed_field": None,
            "_embedded": {
                "verification_type": {
                    "id": 1,
                    "name": "Source Data Verification",
                    "is_sdv": True,
                    "_links": [],
                }
            },
            "_links": [],
        }
    ]

    empty_verification_data = []

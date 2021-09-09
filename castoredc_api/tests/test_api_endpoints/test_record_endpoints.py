# -*- coding: utf-8 -*-
"""
Testing class for record endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/record

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
import random

from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import record_model
from castoredc_api import CastorException


def create_record(fake):
    if fake:
        institute = "FAKE5802-0B07-471F-B97E-B5166332F2C5"
    else:
        institute = "1CFF5802-0B07-471F-B97E-B5166332F2C5"
    return {
        "institute_id": institute,
        "email": "totallyfake@fakeemail.com",
        "record_id": str(random.randint(100000, 999999)),
        "ccr_patient_id": None,
    }


class TestRecord:
    model_keys = record_model.keys()

    test_record = {
        "id": "000006",
        "record_id": "000006",
        "ccr_patient_id": "",
        "last_opened_step": "FFF23B2C-AEE6-4304-9CC4-9C7C431D5387",
        "progress": 10,
        "status": "open",
        "archived": False,
        "archived_reason": None,
        "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "created_on": {
            "date": "2019-10-28 15:24:02.000000",
            "timezone_type": 3,
            "timezone": "Europe/Amsterdam",
        },
        "updated_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "updated_on": {
            "date": "2020-07-03 14:13:44.000000",
            "timezone_type": 3,
            "timezone": "Europe/Amsterdam",
        },
        "randomized_id": None,
        "randomized_on": None,
        "randomization_group": None,
        "randomization_group_name": None,
        "_embedded": {
            "institute": {
                "id": "1CFF5802-0B07-471F-B97E-B5166332F2C5",
                "institute_id": "1CFF5802-0B07-471F-B97E-B5166332F2C5",
                "name": "Test Institute",
                "abbreviation": "TES",
                "code": "TES",
                "order": 0,
                "deleted": False,
                "country_id": 169,
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/institute/1CFF5802-0B07-471F-B97E-B5166332F2C5"
                    }
                },
            }
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/record/000006"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_records(self, client):
        """Returns all records in the study."""
        all_records = client.all_records()
        return all_records

    def test_all_records(self, all_records, item_totals):
        """Tests if all records are returned."""
        assert len(all_records) > 0, "No records found in the study, is this right?"
        assert len(all_records) == item_totals("/record")

    def test_all_records_model(self, all_records):
        """Tests the model returned by all records."""
        for record in all_records:
            api_keys = record.keys()
            # Tests if the model length is the same
            assert len(self.model_keys) == len(api_keys)
            # Tests if the model keys and type of values are the same
            for key in self.model_keys:
                assert key in api_keys
                assert type(record[key]) in record_model[key]

    def test_all_records_archived(self, client):
        """Tests if archived records are properly retrieved"""
        all_records = client.all_records(archived=1)
        for record in all_records:
            assert record["archived"] is True

    def test_all_records_not_archived(self, client):
        """Tests if non-archived records are properly retrieved"""
        all_records = client.all_records(archived=0)
        for record in all_records:
            assert record["archived"] is False

    def test_all_records_single_center(self, client):
        """Tests if institute filtering only retrieves records from the given institute."""
        all_records = client.all_records(
            institute_id="1CFF5802-0B07-471F-B97E-B5166332F2C5"
        )
        for record in all_records:
            assert (
                record["_embedded"]["institute"]["id"]
                == "1CFF5802-0B07-471F-B97E-B5166332F2C5"
            )

    def test_all_records_data(self, all_records):
        """Tests the data of the records returned by all_records"""
        # Select a record
        record = all_records[5]
        # Check if the right data is returned.
        assert record == self.test_record

    def test_single_record_success(self, client):
        """Tests if single record returns the proper data."""
        record = client.single_record("000006")
        assert record == self.test_record

    def test_single_record_failure(self, client):
        """Tests if single record returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_record("FAKE06")
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_create_record_success(self, client):
        """Tests creating a new record."""
        len_records = len(client.all_records())

        record = create_record(fake=False)
        created = client.create_record(**record)
        new_record_id = created["id"]

        new_records = client.all_records()
        new_len = len(new_records)

        assert new_len == (len_records + 1)
        assert new_record_id in [record["id"] for record in new_records]

    def test_create_record_fail(self, client):
        """Tests if creating a record for a non-existing institute raises an error."""
        len_records = len(client.all_records())

        record = create_record(fake=True)
        with pytest.raises(HTTPStatusError) as e:
            client.create_record(**record)
        assert "422 Client Error: Unprocessable Entity for url:" in str(e.value)

        new_records = client.all_records()
        new_len = len(new_records)

        assert new_len == len_records

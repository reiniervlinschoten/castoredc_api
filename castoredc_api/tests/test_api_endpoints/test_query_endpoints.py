# -*- coding: utf-8 -*-
"""
Testing class for query endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/query

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import query_model
from castoredc_api import CastorException


class TestQuery:
    model_keys = query_model.keys()

    test_query = {
        "id": "CAEC9130-EBDA-446A-9E21-35FE590C4DE3",
        "record_id": "110001",
        "field_id": "B90870EE-EE37-4AC0-B845-DE428C0E000A",
        "status": "New",
        "first_query_remark": "Quite low, is this right?",
        "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "created_on": {
            "date": "2019-09-23 12:16:37.000000",
            "timezone_type": 3,
            "timezone": "Europe/Amsterdam",
        },
        "updated_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "updated_on": {
            "date": "2019-09-23 12:16:37.000000",
            "timezone_type": 3,
            "timezone": "Europe/Amsterdam",
        },
        "_embedded": {
            "query_remarks": [
                {
                    "id": "BAF66EE9-DB44-48B5-9247-DBED30EFC553",
                    "title": None,
                    "description": "Quite low, is this right?",
                    "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
                    "created_on": {
                        "date": "2019-09-23 12:16:37.000000",
                        "timezone_type": 3,
                        "timezone": "Europe/Amsterdam",
                    },
                    "_links": {
                        "self": {
                            "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/query/BAF66EE9-DB44-48B5-9247-DBED30EFC553"
                        }
                    },
                }
            ]
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/query/CAEC9130-EBDA-446A-9E21-35FE590C4DE3"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_queries(self, client):
        """Get all queries in the study."""
        all_queries = client.all_queries()
        return all_queries

    def test_all_queries(self, all_queries, item_totals):
        """Tests if all queries are returned."""
        assert len(all_queries) > 0, "No queries found in the study, is this right?"
        assert len(all_queries) == item_totals("/query")

    def test_all_queries_model(self, all_queries):
        """Tests the model returned by all_queries."""
        for query in all_queries:
            api_keys = query.keys()
            # Tests if the same number of keys is returned
            assert len(self.model_keys) == len(api_keys)
            # Tests if the keys and types of values are the same
            for key in self.model_keys:
                assert key in api_keys
                assert type(query[key]) in query_model[key]

    def test_all_queries_data(self, all_queries):
        """Tests the data of the queries returned by all_queries"""
        # Select a query
        query = all_queries[0]
        # Check if the right data is returned.
        assert query == self.test_query

    def test_single_query_success(self, client):
        """Tests if single_query returns the proper data."""
        query = client.single_query("CAEC9130-EBDA-446A-9E21-35FE590C4DE3")
        assert query == self.test_query

    def test_single_query_failure(self, client):
        """Tests if single_query returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_query("FAKE9130-EBDA-446A-9E21-35FE590C4DE3")
        assert "404 Client Error: Not Found for url" in str(e.value)

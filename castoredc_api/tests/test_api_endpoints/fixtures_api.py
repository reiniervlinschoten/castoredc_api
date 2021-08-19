from castoredc_api.auth import auth_data

import pytest
from castoredc_api import CastorClient


@pytest.fixture(scope="class")
def client():
    client = CastorClient(
        auth_data.client_id, auth_data.client_secret, "data.castoredc.com"
    )
    client.link_study(auth_data.test_client_study_id)
    return client


@pytest.fixture(scope="class")
def item_totals(client):
    def return_item_totals(endpoint, base=False):
        return client.request_size(endpoint, base)

    return return_item_totals

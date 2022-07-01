import json
import secrets

import httpx
import pytest
from castoredc_api import CastorClient
from pytest_httpx import HTTPXMock


@pytest.fixture
def mock_auth(httpx_mock):
    def token_response(httpx_mock: HTTPXMock):
        return httpx.Response(
            status_code=200,
            json={
                "access_token": secrets.token_hex(32),
                "expires_in": 18000,
                "token_type": "Bearer",
                "scope": "default",
            },
        )

    httpx_mock.add_callback(
        url="https://data.castoredc.com/oauth/token",
        callback=token_response,
    )
    return httpx_mock


def test_clients_are_distinct(mock_auth):
    client1 = CastorClient(
        "DUMMY_CLIENT_ID", "DUMMY_CLIENT_SECRET", "data.castoredc.com"
    )
    client2 = CastorClient(
        "DUMMY_CLIENT_ID", "DUMMY_CLIENT_SECRET", "data.castoredc.com"
    )

    assert client1.headers is not client2.headers

import json
import secrets
import sys

import httpx
import pytest
from castoredc_api import CastorClient
from pytest_httpx import HTTPXMock

if sys.version_info >= (3, 8):
    from importlib import metadata as pkg_metadata
else:
    import importlib_metadata as pkg_metadata


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


def test_client_sets_correct_user_agent(httpx_mock, mock_auth):
    # This makes an HTTP request on instantiation to exchange client secrets
    # for a token, so there's no need to make another HTTP request in this test.
    _ = CastorClient("DUMMY_CLIENT_ID", "DUMMY_CLIENT_SECRET", "data.castoredc.com")

    assert (
        httpx_mock.get_request().headers["user-agent"]
        == f"python-castoredc_api/{pkg_metadata.version('castoredc_api')}"
    )

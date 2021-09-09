# -*- coding: utf-8 -*-
"""
Testing class for user endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/user

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api import CastorException
from castoredc_api.tests.test_api_endpoints.data_models import user_model


class TestUser:
    model_keys = user_model.keys()

    @pytest.fixture(scope="class")
    def all_users(self, client):
        """Returns all users"""
        all_users = client.all_users()
        return all_users

    def test_all_users(self, all_users):
        """Tests if all_users returns the correct model"""
        assert len(all_users) > 0
        for user in all_users:
            api_keys = user.keys()
            assert len(api_keys) == len(self.model_keys)
            for key in api_keys:
                assert key in self.model_keys
                assert type(user[key]) in user_model[key]

    def test_single_user_success(self, client, all_users):
        """Tests if single_user returns the correct model"""
        user = client.single_user(all_users[0]["id"])
        api_keys = user.keys()
        assert len(api_keys) == len(self.model_keys)
        for key in api_keys:
            assert key in self.model_keys
            assert type(user[key]) in user_model[key]

    def test_single_user_fail(self, client, all_users):
        """Tests if single_user fails correctly"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_user(all_users[0]["id"] + "FAKE")
        assert "403 Client Error: Forbidden for url" in str(e.value)

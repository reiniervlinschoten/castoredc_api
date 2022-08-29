# -*- coding: utf-8 -*-
"""
Testing class for step endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/step

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import role_model


class TestStep:
    model_keys = role_model.keys()
    test_role = {
        "name": "Admin",
        "description": "",
        "permissions": {
            "add": True,
            "view": True,
            "edit": True,
            "delete": True,
            "lock": True,
            "query": True,
            "export": True,
            "randomization_read": True,
            "randomization_write": True,
            "sign": True,
            "email_addresses": True,
            "sdv": True,
            "survey_send": True,
            "survey_view": True,
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001/role/Admin"
            }
        },
    }

    @pytest.fixture(scope="function")
    def all_roles(self, write_client):
        """Returns all study roles."""
        all_roles = write_client.all_roles()
        return all_roles

    def test_all_roles_amount(self, all_roles, item_totals, write_client):
        """Tests if all_steps returns all steps from the study."""
        assert len(all_roles) > 0, "No roles found in the study, is this right?"
        assert len(all_roles) == write_client.request_size("/role", False)

    def test_all_roles_model(self, all_roles):
        """Tests the model of all study steps."""
        for role in all_roles:
            role_keys = role.keys()
            # Tests if the same number of keys is returned
            assert len(role_keys) == len(self.model_keys)
            # Tests if every key and value type is the same
            for key in role_keys:
                assert key in self.model_keys
                assert type(role[key]) in role_model[key]

    def test_all_roles_data(self, all_roles):
        """Tests the data of all study roles."""
        assert all_roles[0] == self.test_role

    def test_single_role_success(self, write_client):
        """Test retrieving a single role."""
        role = write_client.single_role("ADMIN")
        assert role == self.test_role

    def test_single_step_fail(self, write_client):
        """Test failing to retrieve a single role."""
        with pytest.raises(HTTPStatusError) as e:
            write_client.single_step("FAKE")
        assert e.value.response.status_code == 404

    def test_create_role_success(self, write_client):
        """Test successfully creating a new role"""
        body = {
            "name": "API Tester",
            "description": "Role for testing the API",
            "permissions": {
                "add": True,
                "view": True,
                "edit": True,
                "delete": True,
                "lock": True,
                "query": True,
                "export": True,
                "randomization_read": True,
                "sign": True,
                "email_addresses": True,
                "randomization_write": True,
                "sdv": True,
                "survey_send": True,
                "survey_view": True,
            },
        }
        with pytest.raises(HTTPStatusError) as e:
            write_client.create_role(**body)
        assert e.value.response.status_code == 422
        # User already exists
        assert "User Role name already exists." in e.value.response.json()["detail"]

    def test_create_role_fail(self, write_client):
        """Test failing to create a new role"""
        body = {
            "name": "Error Role",
            "description": "Fails because of integers instead of bools",
            "permissions": {
                "add": True,
                "view": 5,
                "edit": True,
                "delete": True,
                "lock": True,
                "query": 33,
                "export": True,
                "randomization_read": True,
                "sign": True,
                "email_addresses": True,
                "randomization_write": 1,
                "sdv": True,
                "survey_send": True,
                "survey_view": True,
            },
        }
        with pytest.raises(HTTPStatusError) as e:
            write_client.create_role(**body)
        assert e.value.response.status_code == 400
        # User already exists
        assert "Invalid request parameters" in e.value.response.json()["detail"]

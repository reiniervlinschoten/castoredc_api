# -*- coding: utf-8 -*-
"""
Testing class for study endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/study

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import (
    study_model,
    user_study_model,
)


class TestStudy:
    s_model_keys = study_model.keys()
    u_model_keys = user_study_model.keys()

    test_study = {
        "crf_id": "1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001",
        "study_id": "1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001",
        "name": "PythonWrapperTest - Client (Write)",
        "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "created_on": "2022-06-28 07:13:41",
        "trial_registry_id": "",
        "live": True,
        "randomization_enabled": True,
        "gcp_enabled": True,
        "surveys_enabled": True,
        "premium_support_enabled": False,
        "main_contact": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "expected_centers": 1,
        "expected_records": 100,
        "slug": "8pDFJAdy4m3Kf8fZEMRxw6",
        "version": "0.01",
        "duration": 24,
        "domain": "https://data.castoredc.com",
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001"
            }
        },
    }

    @pytest.fixture(scope="function")
    def all_studies(self, write_client):
        """Get all studies."""
        all_studies = write_client.all_studies()
        return all_studies

    def test_all_studies_amount(self, all_studies, write_client):
        """Checks if the right number of studies is returned."""
        assert len(all_studies) > 0, "No studies found for this user, is this right?"
        total_users = write_client.request_size("/study", base=True)
        assert len(all_studies) == total_users

    def test_all_studies_model(self, all_studies):
        """Test the model of the studies returned."""
        for study in all_studies:
            study_keys = study.keys()
            # Tests whether the right number of keys is returned
            assert len(study_keys) == len(self.s_model_keys)
            # Test whether the keys and value types are right
            for key in study_keys:
                assert key in self.s_model_keys
                assert type(study[key]) in study_model[key]

    def test_all_studies_data(self, all_studies):
        """Tests the data of the studies returned by all_studies"""
        # Select a study
        study = all_studies[1]
        # Check if the right data is returned.
        assert study == self.test_study

    def test_single_study_success(self, write_client):
        """Tests returning a single study"""
        study = write_client.single_study("1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001")
        assert study == self.test_study

    def test_single_study_fail(self, write_client):
        """Tests failing to return a study"""
        with pytest.raises(HTTPStatusError) as e:
            write_client.single_study("D234215B-D956-482D-BF17-71F2BB12FAKE")
        assert e.value.response.status_code == 404

    def test_all_users_success(self, write_client):
        """Tests if the API returns all users belonging to a study"""
        total_users = write_client.request_size(
            "/study/1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001/user", base=True
        )
        all_users = write_client.all_users_study("1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001")
        # Tests if the right number of users is returned
        assert len(all_users) == total_users
        for user in all_users:
            user_keys = user.keys()
            # Tests if the right keys and value types are returned
            assert len(user_keys) == len(self.u_model_keys)
            for key in user_keys:
                assert key in self.u_model_keys
                assert type(user[key]) in user_study_model[key]

    def test_all_users_fail(self, write_client):
        """Tests failing to return all users for a study"""
        with pytest.raises(HTTPStatusError) as e:
            write_client.all_users_study("D234215B-D956-482D-BF17-71F2BB12FAKE")
        assert e.value.response.status_code == 404

    def test_single_user_success(self, write_client):
        """Tests returning a single user"""
        user = write_client.single_user_study(
            "1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001",
            "06A8C79E-F76F-4824-AB1A-93F0457C5A61",
        )
        user_keys = user.keys()
        # Tests if the right keys and value types are returned
        assert len(user_keys) == len(self.u_model_keys)
        for key in user_keys:
            assert key in self.u_model_keys
            assert type(user[key]) in user_study_model[key]

    def test_single_user_fail(self, all_studies, write_client):
        """Tests failing to return a single user"""
        with pytest.raises(HTTPStatusError) as e:
            write_client.single_user_study(
                "1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001",
                "B23ABCC4-3A53-FB32-7B78-3960CC90FAKE",
            )
        assert e.value.response.status_code == 404

    def test_invite_user_success(self, write_client):
        """Tests inviting a user to the study"""
        body = {
            "institute_id": "EBCA14F3-56E9-4F7A-9AD6-DD6E5C41A632",
            "email": "castoredcapi.github@gmail.com",
            "message": "Testing API",
        }
        with pytest.raises(HTTPStatusError) as e:
            write_client.invite_user_study(
                "1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001", **body
            )
        assert e.value.response.status_code == 400
        # User already exists
        assert (
            "Could not send an email to the added user."
            in e.value.response.json()["detail"]
        )

    def test_invite_user_success_permissions(self, write_client):
        """Tests inviting a user to the study"""
        body = {
            "institute_id": "EBCA14F3-56E9-4F7A-9AD6-DD6E5C41A632",
            "email": "castoredcapi.github@gmail.com",
            "message": "Testing API",
            "manage_permissions": {
                "manage_form": True,
                "manage_users": True,
                "manage_settings": True,
                "manage_encryption": True,
                "manage_records": True,
            },
            "institute_permissions": [
                {
                    "institute_id": "EBCA14F3-56E9-4F7A-9AD6-DD6E5C41A632",
                    "role": None,
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
                        "encrypt": True,
                        "decrypt": True,
                        "email_addresses": True,
                        "sdv": True,
                        "survey_send": True,
                        "survey_view": True,
                    },
                }
            ],
        }
        with pytest.raises(HTTPStatusError) as e:
            write_client.invite_user_study(
                "1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001", **body
            )
        assert e.value.response.status_code == 400
        # User already exists
        assert (
            "Could not send an email to the added user."
            in e.value.response.json()["detail"]
        )

    def test_invite_user_fail_permissions(self, write_client):
        """Tests inviting a user to the study"""
        body = {
            "institute_id": "EBCA14F3-56E9-4F7A-9AD6-DD6E5C41A632",
            "email": "fake@emailfakeemail.com",
            "message": "Testing API",
            "manage_permissions": {
                "manage_form": True,
                "manage_users": True,
                "manage_settings": True,
                "manage_encryption": True,
                "manage_records": True,
            },
            "institute_permissions": [
                {
                    "institute_id": "FAKEA79-E02E-4545-9719-95B8DDED9108",
                    "role": None,
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
                        "encrypt": True,
                        "decrypt": True,
                        "email_addresses": True,
                        "sdv": True,
                        "survey_send": True,
                        "survey_view": True,
                    },
                }
            ],
        }
        with pytest.raises(HTTPStatusError) as e:
            write_client.invite_user_study(
                "1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001", **body
            )
        assert e.value.response.status_code == 400
        # Permissions are wonky, but gives a non-informative error at Castor
        assert (
            "Could not send an email to the added user."
            in e.value.response.json()["detail"]
        )

    def test_invite_user_fail(self, write_client):
        """Tests failing to invite a user"""
        body = {
            "institute_id": "FAKE6A79-E02E-4545-9719-95B8DDED9108",
            "email": "castoredcapi.github@gmail.com",
            "message": "Testing API",
        }
        with pytest.raises(HTTPStatusError) as e:
            write_client.invite_user_study(
                "1BCD52D3-7AB3-4EA9-8ABE-74B4B7087001", **body
            )
        assert e.value.response.status_code == 400
        assert "BAD_REQUEST" in e.value.response.json()["detail"]

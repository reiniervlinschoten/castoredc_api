# -*- coding: utf-8 -*-
"""
Testing class for study endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/study

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api import CastorException
from castoredc_api.tests.test_api_endpoints.data_models import study_model, user_model


class TestStudy:
    s_model_keys = study_model.keys()
    u_model_keys = user_model.keys()

    test_study = {
        "crf_id": "D234215B-D956-482D-BF17-71F2BB12A2FD",
        "study_id": "D234215B-D956-482D-BF17-71F2BB12A2FD",
        "name": "PythonWrapperTest - Client",
        "created_by": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "created_on": "2019-09-23 10:12:48",
        "live": True,
        "randomization_enabled": True,
        "gcp_enabled": True,
        "surveys_enabled": True,
        "premium_support_enabled": False,
        "main_contact": "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        "expected_centers": 2,
        "expected_records": 50,
        "slug": "python-wrapper",
        "version": "0.61",
        "duration": 15,
        "domain": "https://data.castoredc.com",
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_studies(self, client):
        """Get all studies."""
        all_studies = client.all_studies()
        return all_studies

    def test_all_studies_amount(self, all_studies, client):
        """Checks if the right number of studies is returned."""
        assert len(all_studies) > 0, "No studies found for this user, is this right?"
        total_users = client.request_size("/study", base=True)
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
        study = all_studies[2]
        # Check if the right data is returned.
        assert study == self.test_study

    def test_single_study_success(self, all_studies, client):
        """Tests returning a single study"""
        study = client.single_study("D234215B-D956-482D-BF17-71F2BB12A2FD")
        assert study == self.test_study

    def test_single_study_fail(self, all_studies, client):
        """Tests failing to return a study"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_study("D234215B-D956-482D-BF17-71F2BB12FAKE")
        assert "403 Client Error: Forbidden for url" in str(e.value)

    def test_all_users_success(self, all_studies, client):
        """Tests if the API returns all users belonging to a study"""
        total_users = client.request_size(
            "/study/D234215B-D956-482D-BF17-71F2BB12A2FD/user", base=True
        )
        all_users = client.all_users_study("D234215B-D956-482D-BF17-71F2BB12A2FD")
        # Tests if the right number of users is returned
        assert len(all_users) == total_users
        for user in all_users:
            user_keys = user.keys()
            # Tests if the right keys and value types are returned
            assert len(user_keys) == len(self.u_model_keys)
            for key in user_keys:
                assert key in self.u_model_keys
                assert type(user[key]) in user_model[key]

    def test_all_users_fail(self, all_studies, client):
        """Tests failing to return all users for a study"""
        with pytest.raises(HTTPStatusError) as e:
            client.all_users_study("D234215B-D956-482D-BF17-71F2BB12FAKE")
        assert "403 Client Error: Forbidden for url" in str(e.value)

    def test_single_user_success(self, all_studies, client):
        """Tests returning a single user"""
        user = client.single_user_study(
            "D234215B-D956-482D-BF17-71F2BB12A2FD",
            "B23ABCC4-3A53-FB32-7B78-3960CC907F25",
        )
        user_keys = user.keys()
        # Tests if the right keys and value types are returned
        assert len(user_keys) == len(self.u_model_keys)
        for key in user_keys:
            assert key in self.u_model_keys
            assert type(user[key]) in user_model[key]

    def test_single_user_fail(self, all_studies, client):
        """Tests failing to return a single user"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_user_study(
                "D234215B-D956-482D-BF17-71F2BB12A2FD",
                "B23ABCC4-3A53-FB32-7B78-3960CC90FAKE",
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

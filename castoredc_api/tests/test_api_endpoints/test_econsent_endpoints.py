# -*- coding: utf-8 -*-
"""
Testing class for participant_econsent endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/participant-econsent

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.test_record_endpoints import create_record


class TestEconsent:
    @pytest.mark.xfail(
        reason="Econsent not enabled on testing databases",
        strict=True,
    )
    def test_econsent_get_success(self, client):
        """Tests if econsent returns the proper data."""
        response = client.get_econsent("000024")
        assert response == {
            "econsent_subject_id": "SUBJECTID",
            "econsent_study_id": "STUDYID",
            "econsent_region": "STUDYREGION",
        }

    def test_econsent_get_failure(self, client):
        """Tests if single token returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.get_econsent("FAKE24")
        assert e.value.response.status_code == 404

    @pytest.mark.xfail(
        reason="Econsent not enabled on testing databases",
        strict=True,
    )
    def test_econsent_post_success(self, client):
        """Tests if econsent returns the proper data."""
        response = client.create_econsent(
            "000024",
            **{
                "econsent_subject_id": "SUBJECTID",
                "econsent_study_id": "STUDYID",
                "econsent_region": "STUDYREGION",
            }
        )
        assert response == {
            "econsent_subject_id": "SUBJECTID",
            "econsent_study_id": "STUDYID",
            "econsent_region": "STUDYREGION",
        }

    @pytest.mark.xfail(
        reason="Econsent not enabled on testing databases",
        strict=True,
    )
    def test_econsent_post_failure(self, client):
        """Tests if single token returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.create_econsent(
                "000024",
                **{
                    "econsent_subject_id": "SUBJECTID",
                    "econsent_study_id": "STUDYID",
                    "econsent_region": "STUDYREGION",
                }
            )
        assert e.value.response.status_code == 404

    @pytest.mark.xfail(
        reason="Econsent not enabled on testing databases",
        strict=True,
    )
    def test_econsent_patch_success(self, client):
        """Tests if econsent returns the proper data."""
        response = client.update_econsent(
            "000024",
            **{
                "econsent_subject_id": "SUBJECTID",
                "econsent_study_id": "STUDYID",
                "econsent_region": "STUDYREGION",
            }
        )
        assert response == {
            "econsent_subject_id": "SUBJECTID",
            "econsent_study_id": "STUDYID",
            "econsent_region": "STUDYREGION",
        }

    @pytest.mark.xfail(
        reason="Econsent not enabled on testing databases",
        strict=True,
    )
    def test_econsent_patch_failure(self, client):
        """Tests if single token returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.update_econsent(
                "000024",
                **{
                    "econsent_subject_id": "SUBJECTID",
                    "econsent_study_id": "STUDYID",
                    "econsent_region": "STUDYREGION",
                }
            )
        assert e.value.response.status_code == 404

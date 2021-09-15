# -*- coding: utf-8 -*-
"""
Testing class for survey step endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/survey-step

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api import CastorException
from castoredc_api.tests.test_api_endpoints.data_models import survey_step_model


class TestSurveyStep:
    model_keys = survey_step_model.keys()

    test_survey_step = {
        "id": "C19211FE-1C53-43F9-BC85-460DF1255153",
        "survey_step_id": "C19211FE-1C53-43F9-BC85-460DF1255153",
        "survey_step_name": "Questions about your well-being",
        "survey_step_description": "The steps in a survey represent survey pages.",
        "survey_step_number": 1,
        "_embedded": {
            "survey": {
                "id": "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
                "survey_id": "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
                "name": "QOL Survey",
                "description": "",
                "intro_text": "##### This is the survey intro text. Here you can add some information for the participant that they will see before they start filling in the survey.\n```\n\n\n```\n##### Check the help text in the survey form editor to see how you can format this text or add images and links.\n```\n\n\n```\n### For example, you can use hashtags to make the text bigger or add headings.",
                "outro_text": "",
                "survey_steps": [],
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/survey/D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E"
                    }
                },
            }
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/survey/D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E/survey-step/C19211FE-1C53-43F9-BC85-460DF1255153"
            }
        },
    }

    @pytest.fixture(scope="class")
    def surveys_with_steps(self, client):
        """Returns all surveys with their corresponding steps"""
        surveys_with_steps = {}
        all_surveys = client.all_surveys()
        for survey in all_surveys:
            steps = client.single_survey_all_steps(survey["id"])
            surveys_with_steps[survey["id"]] = steps
        return surveys_with_steps

    def test_all_survey_steps_model(self, surveys_with_steps):
        """Tests if the model of survey steps is right"""
        for survey in surveys_with_steps:
            assert len(surveys_with_steps[survey]) > 0
            for step in surveys_with_steps[survey]:
                assert len(step) == len(self.model_keys)
                api_keys = step.keys()
                for key in self.model_keys:
                    assert key in api_keys
                    assert type(step[key]) in survey_step_model[key]

    def test_all_survey_steps_data(self, surveys_with_steps):
        """Tests if the data of survey steps is right"""
        assert (
            surveys_with_steps["D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E"][0]
            == self.test_survey_step
        )

    def test_single_survey_single_step_success(self, client, surveys_with_steps):
        """Tests whether single step returns the right data"""
        step = client.single_survey_single_step(
            "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
            "C19211FE-1C53-43F9-BC85-460DF1255153",
        )
        assert step == self.test_survey_step

    def test_single_survey_single_step_fail(self, client, surveys_with_steps):
        """Tests whether single step fails correctly"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_survey_single_step(
                "D70C1273-B5D8-45CD-BFE8-A0BA75C44B7E",
                "C19211FE-1C53-43F9-BC85-460DF125FAKE",
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

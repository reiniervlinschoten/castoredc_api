# -*- coding: utf-8 -*-
"""
Testing class for step endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/step

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import study_step_model
from castoredc_api import CastorException


class TestStep:
    model_keys = study_step_model.keys()
    test_step = {
        "id": "F6BB55C9-FC35-4375-86D0-A4F5E239BCB1",
        "step_id": "F6BB55C9-FC35-4375-86D0-A4F5E239BCB1",
        "step_name": "Physical exam",
        "step_order": 8,
        "step_description": "This is a copy of the Baseline Physical exam step.",
        "_embedded": {
            "phase": {
                "id": "B153A407-8D0A-4174-B632-B89AADE3646B",
                "phase_id": "B153A407-8D0A-4174-B632-B89AADE3646B",
                "phase_description": None,
                "phase_name": "Follow-up Visit",
                "phase_duration": None,
                "phase_order": 3,
                "_links": {
                    "self": {
                        "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/phase/B153A407-8D0A-4174-B632-B89AADE3646B"
                    }
                },
            }
        },
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/step/F6BB55C9-FC35-4375-86D0-A4F5E239BCB1"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_steps(self, client):
        """Returns all study steps."""
        all_steps = client.all_steps()
        return all_steps

    def test_all_steps_amount(self, all_steps, item_totals):
        """Tests if all_steps returns all steps from the study."""
        assert len(all_steps) > 0, "No steps found in the study, is this right?"
        assert len(all_steps) == item_totals("/step")

    def test_all_steps_model(self, all_steps):
        """Tests the model of all study steps."""
        for step in all_steps:
            step_keys = step.keys()
            # Tests if the same number of keys is returned
            assert len(step_keys) == len(self.model_keys)
            # Tests if every key and value type is the same
            for key in step_keys:
                assert key in self.model_keys
                assert type(step[key]) in study_step_model[key]

    def test_all_steps_data(self, all_steps):
        """Tests the data of all study steps."""
        assert all_steps[9] == self.test_step

    def test_single_step_success(self, all_steps, client):
        """Test a single step."""
        step = client.single_step("F6BB55C9-FC35-4375-86D0-A4F5E239BCB1")
        assert step == self.test_step

    def test_single_step_fail(self, all_steps, client):
        with pytest.raises(HTTPStatusError) as e:
            client.single_step("F6BB55C9-FC35-4375-86D0-A4F5E239FAKE")
        assert "404 Client Error: Not Found for url" in str(e.value)

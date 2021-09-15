# -*- coding: utf-8 -*-
"""
Testing class for phase endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/phase

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import phase_model
from castoredc_api import CastorException


class TestPhase:
    model_keys = phase_model.keys()

    test_phase = {
        "id": "AA99795D-4F8D-4B4A-96A1-14D026D0328E",
        "phase_id": "AA99795D-4F8D-4B4A-96A1-14D026D0328E",
        "phase_description": None,
        "phase_name": "Unscheduled visits and Medication",
        "phase_duration": None,
        "phase_order": 4,
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D-BF17-71F2BB12A2FD/phase/AA99795D-4F8D-4B4A-96A1-14D026D0328E"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_phases(self, client):
        """Get all phases in the study."""
        all_phases = client.all_phases()
        return all_phases

    def test_all_phases(self, all_phases, item_totals):
        """Tests if all_phases returns all phases from the study."""
        assert len(all_phases) > 0, "No phases found in the study, is this right?"
        assert len(all_phases) == item_totals("/phase")

    def test_all_phases_model(self, all_phases):
        """Tests the model returned by all_phases"""
        for phase in all_phases:
            api_keys = phase.keys()
            # Tests if the same number of keys is returned
            assert len(self.model_keys) == len(api_keys)
            # Tests if every key and value type is the same
            for key in self.model_keys:
                assert key in api_keys
                assert type(phase[key]) in phase_model[key]

    def test_all_phases_data(self, all_phases):
        """Tests the data of the phases returned by all_phases"""
        # Select a phase
        phase = all_phases[2]
        # Check if the right data is returned.
        assert phase == self.test_phase

    def test_single_phase_success(self, client):
        """Tests if single phase returns the proper data."""
        phase = client.single_phase("AA99795D-4F8D-4B4A-96A1-14D026D0328E")
        assert phase == self.test_phase

    def test_single_phase_failure(self, client):
        """Tests if single phase returns an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_phase("FAKE95D-4F8D-4B4A-96A1-14D026D0328E")
        assert "404 Client Error: Not Found for url" in str(e.value)

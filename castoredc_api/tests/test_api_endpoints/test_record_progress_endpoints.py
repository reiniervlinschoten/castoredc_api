# -*- coding: utf-8 -*-
"""
Testing class for record progress endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/record-progress

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest

from castoredc_api.tests.test_api_endpoints.data_models import (
    record_progress_model,
    steps_model,
)


class TestRecordProgress:
    record_progress_keys = record_progress_model.keys()
    steps_keys = steps_model.keys()

    @pytest.fixture(scope="class")
    def progress_report(self, client):
        """Get all progress reports from the study."""
        progress_report = client.record_progress()
        return progress_report

    @pytest.mark.xfail(reason="Castor API Error - Should be paged", strict=True)
    def test_record_progress(self, progress_report, client):
        """Tests if all progress reports are properly retrieved."""
        # Tests if progress reports are retrieved for all non-archived recodrs
        assert len(progress_report) == len(client.all_records(archived=0))

        for record in progress_report:
            api_record_keys = record.keys()
            # Tests if the models are of the same length
            assert len(api_record_keys) == len(self.record_progress_keys)

            # Tests if the same same keys and type of values are retrieved for the record.
            for key in api_record_keys:
                assert key in self.record_progress_keys
                assert type(record[key]) in record_progress_model[key]

                # Tests if the same same keys and type of values are retrieved for the steps within a record.
                for step in record["steps"]:
                    api_step_keys = step.keys()
                    assert len(api_step_keys) == len(self.steps_keys)
                    for step_key in api_step_keys:
                        assert step_key in self.steps_keys
                        assert type(step[step_key]) in steps_model[step_key]

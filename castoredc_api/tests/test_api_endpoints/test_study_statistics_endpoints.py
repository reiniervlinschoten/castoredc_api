# -*- coding: utf-8 -*-
"""
Testing class for statistics endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/study

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest

from castoredc_api.tests.test_api_endpoints.data_models import (
    statistics_model,
    stats_records_model,
    stats_institutes_model,
)


class TestStatistics:
    s_model_keys = statistics_model.keys()
    r_model_keys = stats_records_model.keys()
    i_model_keys = stats_institutes_model.keys()

    @pytest.fixture(scope="class")
    def stats(self, client):
        """Returns study statistics"""
        stats = client.statistics()
        return stats

    def test_study_statistics(self, stats):
        """Tests whether the study statistics model is right."""
        stats_keys = stats.keys()
        assert len(stats_keys) == len(self.s_model_keys)
        for key in stats_keys:
            assert key in self.s_model_keys
            assert type(stats[key]) in statistics_model[key]

    def test_study_statistics_records(self, stats):
        """Tests whether the record model is right"""
        records = stats["records"]
        records_keys = records.keys()
        assert len(records_keys) == len(self.r_model_keys)
        for key in records_keys:
            assert key in self.r_model_keys
            assert type(records[key]) in stats_records_model[key]

    def test_study_statistics_institutes(self, stats):
        """Tests whether the institute models are right"""
        institutes = stats["records"]["institutes"]
        for institute in institutes:
            institute_keys = institute.keys()
            assert len(institute_keys) == len(self.i_model_keys)
            for key in institute_keys:
                assert key in self.i_model_keys
                assert type(institute[key]) in stats_institutes_model[key]

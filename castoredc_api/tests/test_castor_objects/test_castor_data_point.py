# -*- coding: utf-8 -*-
"""
Testing class for the CastorDataPoint class.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import numpy as np
import pytest

from castoredc_api.study.castor_objects.castor_data_point import CastorDataPoint
from castoredc_api import CastorException


class TestCastorDataPoint:
    """Testing class for CastorDataPoint object unit tests."""

    def test_data_point_create(self, complete_study):
        """Tests creation of a data point."""
        data_point = CastorDataPoint(
            "FAKE-STUDY-FIELD-ID4", "test", complete_study, "2021-01-15 13:39:47"
        )
        assert type(data_point) is CastorDataPoint
        assert data_point.field_id == "FAKE-STUDY-FIELD-ID4"
        assert data_point.raw_value == "test"
        assert data_point.instance_of.field_id == "FAKE-STUDY-FIELD-ID4"

    def test_data_point_create_fail(self, complete_study):
        """Tests failure of creation of a data point."""
        with pytest.raises(CastorException) as e:
            CastorDataPoint(
                "FAKE-STUDY-FIELD-ID8", "test", complete_study, "2021-01-15 13:39:47"
            )
        assert (
            str(e.value)
            == "The field that this is an instance of does not exist in the study!"
        )

    def test_data_point_missing_data_checkbox(self, missing_data_study):
        """Tests if missing data is handled correctly"""
        field_types = ["checkbox"]
        for field_type in field_types:
            for missing_type, formatted in {
                "": "",
                "Missing (measurement failed)": "measurement failed",
                "Missing (not applicable)": "not applicable",
                "Missing (not asked)": "not asked",
                "Missing (asked but unknown)": "asked but unknown",
                "Missing (not done)": "not done",
            }.items():
                data_point = CastorDataPoint(
                    f"MISSING-{field_type}-ID",
                    missing_type,
                    missing_data_study,
                    "2021-01-15 13:39:47",
                )
                assert data_point.value == formatted

    def test_data_point_missing_data_numeric(self, missing_data_study):
        """Tests if missing data is handled correctly"""
        field_types = ["numeric", "year"]
        for field_type in field_types:
            for missing_type, formatted in {
                "": np.nan,
                "Missing (measurement failed)": -95,
                "Missing (not applicable)": -96,
                "Missing (not asked)": -97,
                "Missing (asked but unknown)": -98,
                "Missing (not done)": -99,
            }.items():
                data_point = CastorDataPoint(
                    f"MISSING-{field_type}-ID",
                    missing_type,
                    missing_data_study,
                    "2021-01-15 13:39:47",
                )
                if missing_type == "":
                    assert data_point.value is formatted
                else:
                    assert data_point.value == formatted

    def test_data_point_missing_data_time(self, missing_data_study):
        """Tests if missing data is handled correctly"""
        field_types = ["time"]
        for field_type in field_types:
            for missing_type, formatted in {
                "": "",
                "Missing (measurement failed)": "-95",
                "Missing (not applicable)": "-96",
                "Missing (not asked)": "-97",
                "Missing (asked but unknown)": "-98",
                "Missing (not done)": "-99",
            }.items():
                data_point = CastorDataPoint(
                    f"MISSING-{field_type}-ID",
                    missing_type,
                    missing_data_study,
                    "2021-01-15 13:39:47",
                )
                assert data_point.value == formatted

    def test_data_point_missing_data_date(self, missing_data_study):
        """Tests if missing data is handled correctly"""
        field_types = ["date"]
        for field_type in field_types:
            for missing_type, formatted in {
                "": np.nan,
                "Missing (measurement failed)": "01-01-2995",
                "Missing (not applicable)": "01-01-2996",
                "Missing (not asked)": "01-01-2997",
                "Missing (asked but unknown)": "01-01-2998",
                "Missing (not done)": "01-01-2999",
            }.items():
                data_point = CastorDataPoint(
                    f"MISSING-{field_type}-ID",
                    missing_type,
                    missing_data_study,
                    "2021-01-15 13:39:47",
                )
                if missing_type == "":
                    assert data_point.value is formatted
                else:
                    assert data_point.value == formatted

    def test_data_point_missing_data_datetime(self, missing_data_study):
        """Tests if missing data is handled correctly"""
        field_types = ["datetime"]
        for field_type in field_types:
            for missing_type, formatted in {
                "": np.nan,
                "Missing (measurement failed)": "01-01-2995 00:00",
                "Missing (not applicable)": "01-01-2996 00:00",
                "Missing (not asked)": "01-01-2997 00:00",
                "Missing (asked but unknown)": "01-01-2998 00:00",
                "Missing (not done)": "01-01-2999 00:00",
            }.items():
                data_point = CastorDataPoint(
                    f"MISSING-{field_type}-ID",
                    missing_type,
                    missing_data_study,
                    "2021-01-15 13:39:47",
                )
                if missing_type == "":
                    assert data_point.value is formatted
                else:
                    assert data_point.value == formatted

    def test_data_point_missing_data_numberdate(self, missing_data_study):
        """Tests if missing data is handled correctly"""
        field_types = ["numberdate"]
        for field_type in field_types:
            for missing_type, formatted in {
                "": [np.nan, np.nan],
                "Missing (measurement failed)": [-95, "01-01-2995"],
                "Missing (not applicable)": [-96, "01-01-2996"],
                "Missing (not asked)": [-97, "01-01-2997"],
                "Missing (asked but unknown)": [-98, "01-01-2998"],
                "Missing (not done)": [-99, "01-01-2999"],
            }.items():
                data_point = CastorDataPoint(
                    f"MISSING-{field_type}-ID",
                    missing_type,
                    missing_data_study,
                    "2021-01-15 13:39:47",
                )
                assert data_point.value == formatted

# -*- coding: utf-8 -*-
"""
Testing class for the CastorDataPoint class.

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
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

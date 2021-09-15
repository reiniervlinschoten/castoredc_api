# -*- coding: utf-8 -*-
"""
Testing class for data-point-collection endpoint of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/data-point-collection

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import (
    study_data_point_model,
    report_data_point_model,
    survey_data_point_model,
    survey_package_data_point_model,
)
from castoredc_api.tests.test_api_endpoints.helpers_api_endpoints import allowed_value


class TestDataPoint:
    study_data_point_model_keys = study_data_point_model.keys()
    report_data_point_model_keys = report_data_point_model.keys()
    survey_data_point_model_keys = survey_data_point_model.keys()
    survey_package_data_point_model_keys = survey_package_data_point_model.keys()

    test_report_instance_data_points = [
        {
            "field_id": "05353909-4BFB-4547-8700-AD6755FE82DB",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2019-10-28 14:05:28",
            "report_instance_id": "124EBE17-8AEF-4A74-BBA7-68DF75693FBD",
            "report_instance_name": "46286061",
        },
        {
            "field_id": "345C89CE-4CF9-4C44-8186-CF813EA7C181",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2019-10-28 14:05:28",
            "report_instance_id": "124EBE17-8AEF-4A74-BBA7-68DF75693FBD",
            "report_instance_name": "46286061",
        },
        {
            "field_id": "9E780182-2DF6-423B-A3BE-7934BFED0747",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2019-10-28 14:05:28",
            "report_instance_id": "124EBE17-8AEF-4A74-BBA7-68DF75693FBD",
            "report_instance_name": "46286061",
        },
        {
            "field_id": "9F64DFE1-4C5E-4BCC-93B6-3624FA9FC2A4",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2019-10-28 14:05:28",
            "report_instance_id": "124EBE17-8AEF-4A74-BBA7-68DF75693FBD",
            "report_instance_name": "46286061",
        },
        {
            "field_id": "C8BD45CE-46C3-43D8-BD2A-DF584A046CF7",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2019-10-28 14:05:28",
            "report_instance_id": "124EBE17-8AEF-4A74-BBA7-68DF75693FBD",
            "report_instance_name": "46286061",
        },
        {
            "field_id": "CF963988-E9CE-4CEB-A706-CDFA4916A934",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2019-10-28 14:05:28",
            "report_instance_id": "124EBE17-8AEF-4A74-BBA7-68DF75693FBD",
            "report_instance_name": "46286061",
        },
        {
            "field_id": "F610012E-B618-40A7-AA36-6C8BD959A1F1",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2019-10-28 14:05:28",
            "report_instance_id": "124EBE17-8AEF-4A74-BBA7-68DF75693FBD",
            "report_instance_name": "46286061",
        },
    ]
    test_survey_instance_data_points = [
        {
            "field_id": "5D3843C7-8341-45DD-A769-8A5D24E6CDA5",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2020-08-14 11:59:20",
            "survey_instance_id": "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E",
            "survey_name": "QOL Survey",
        },
        {
            "field_id": "6C87B052-1289-4AB2-8D4F-D15AF4DDF950",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2020-08-14 11:59:20",
            "survey_instance_id": "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E",
            "survey_name": "QOL Survey",
        },
        {
            "field_id": "A6E8C700-1A2B-4A87-AE1F-E8DC2C2F72C2",
            "field_value": "5",
            "record_id": "000005",
            "updated_on": "2020-08-14 11:59:20",
            "survey_instance_id": "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E",
            "survey_name": "QOL Survey",
        },
        {
            "field_id": "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2020-08-14 11:59:20",
            "survey_instance_id": "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E",
            "survey_name": "QOL Survey",
        },
        {
            "field_id": "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
            "field_value": "1",
            "record_id": "000005",
            "updated_on": "2020-08-14 11:59:20",
            "survey_instance_id": "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E",
            "survey_name": "QOL Survey",
        },
    ]
    test_survey_package_data_points = [
        {
            "field_id": "5D3843C7-8341-45DD-A769-8A5D24E6CDA5",
            "field_value": "1",
            "record_id": "000002",
            "updated_on": "2020-05-13 16:17:58",
            "survey_instance_id": "F61EF287-9BD1-4047-AB46-88E0F69DD120",
            "survey_name": "QOL Survey",
            "survey_package_instance_id": "23B4FD48-BA41-4C9B-BAEF-D5C3DD5F8E5C",
        },
        {
            "field_id": "6C87B052-1289-4AB2-8D4F-D15AF4DDF950",
            "field_value": "1",
            "record_id": "000002",
            "updated_on": "2020-05-13 16:17:58",
            "survey_instance_id": "F61EF287-9BD1-4047-AB46-88E0F69DD120",
            "survey_name": "QOL Survey",
            "survey_package_instance_id": "23B4FD48-BA41-4C9B-BAEF-D5C3DD5F8E5C",
        },
        {
            "field_id": "A6E8C700-1A2B-4A87-AE1F-E8DC2C2F72C2",
            "field_value": "5",
            "record_id": "000002",
            "updated_on": "2020-05-13 16:17:58",
            "survey_instance_id": "F61EF287-9BD1-4047-AB46-88E0F69DD120",
            "survey_name": "QOL Survey",
            "survey_package_instance_id": "23B4FD48-BA41-4C9B-BAEF-D5C3DD5F8E5C",
        },
        {
            "field_id": "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
            "field_value": "1",
            "record_id": "000002",
            "updated_on": "2020-05-13 16:17:58",
            "survey_instance_id": "F61EF287-9BD1-4047-AB46-88E0F69DD120",
            "survey_name": "QOL Survey",
            "survey_package_instance_id": "23B4FD48-BA41-4C9B-BAEF-D5C3DD5F8E5C",
        },
        {
            "field_id": "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
            "field_value": "1",
            "record_id": "000002",
            "updated_on": "2020-05-13 16:17:58",
            "survey_instance_id": "F61EF287-9BD1-4047-AB46-88E0F69DD120",
            "survey_name": "QOL Survey",
            "survey_package_instance_id": "23B4FD48-BA41-4C9B-BAEF-D5C3DD5F8E5C",
        },
    ]

    @pytest.fixture(scope="function")
    def all_study_data_points(self, client):
        """Return all study data points"""
        all_study_data_points = client.all_study_data_points()
        return all_study_data_points

    @pytest.fixture(scope="function")
    def all_report_data_points(self, client):
        """Return all study data points"""
        all_report_data_points = client.all_report_data_points()
        return all_report_data_points

    @pytest.fixture(scope="function")
    def all_survey_data_points(self, client):
        """Return all study data points"""
        all_survey_data_points = client.all_survey_data_points()
        return all_survey_data_points

    def test_all_study_data_points_amount(self, all_study_data_points, item_totals):
        """Tests that the all_study_data_points retrieves the same number as data points as Castor says that are in
        the database."""
        assert len(all_study_data_points) == item_totals("/data-point-collection/study")

    def test_all_study_data_points_model(self, all_study_data_points):
        """Tests if the study data point model is the same as the specified model."""
        for i in [5, 100, 233]:  # Only select a subset of the data points
            data_point = all_study_data_points[i]
            api_keys = data_point.keys()
            assert len(self.study_data_point_model_keys) == len(api_keys)
            for key in api_keys:
                assert key in self.study_data_point_model_keys
                assert type(data_point[key]) in study_data_point_model[key]

    def test_all_report_data_points_amount(self, all_report_data_points, item_totals):
        """Tests that the all_report_data_points retrieves the same number as data points as Castor says that are in
        the database."""
        assert len(all_report_data_points) == item_totals(
            "/data-point-collection/report-instance"
        )

    def test_all_report_data_points_model(self, all_report_data_points):
        """Tests if the report data point model is the same as the specified model."""
        for i in [5, 100, 156]:  # Only select a subset of the data points
            data_point = all_report_data_points[i]
            api_keys = data_point.keys()
            assert len(self.report_data_point_model_keys) == len(api_keys)
            for key in api_keys:
                assert key in self.report_data_point_model_keys
                assert type(data_point[key]) in report_data_point_model[key]

    def test_all_survey_data_points_amount(self, all_survey_data_points, item_totals):
        """Tests that the all_survey_data_points retrieves the same number as data points as Castor says that are in
        the database."""
        assert len(all_survey_data_points) == item_totals(
            "/data-point-collection/survey-instance"
        )

    def test_all_survey_data_points_model(self, all_survey_data_points):
        """Tests if the survey data point model is the same as the specified model."""
        for i in [5, 32, 103]:  # Only select a subset of the data points
            data_point = all_survey_data_points[i]
            api_keys = data_point.keys()
            assert len(self.survey_data_point_model_keys) == len(api_keys)
            for key in api_keys:
                assert key in self.survey_data_point_model_keys
                assert type(data_point[key]) in survey_data_point_model[key]

    def test_single_report_instance_data_points_success(self, client):
        """Tests if single_report_instance_data_points returns the proper data."""
        report_data_points = client.single_report_instance_data_points(
            "124EBE17-8AEF-4A74-BBA7-68DF75693FBD"
        )
        assert report_data_points == self.test_report_instance_data_points

    def test_single_report_instance_data_points_fail(self, client):
        """Tests if single_report_instance_data_points throws proper error when non-existing report is called."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_report_instance_data_points(
                "124EBE17-8AEF-4A74-BBA7-68DF7569FAKE"
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

    @pytest.mark.xfail(reason="Castor Database Error", strict=True)
    def test_single_survey_instance_data_points_success(self, client):
        """Tests if single_survey_instance_data_points returns the data points in the proper model."""
        survey_data_points = client.single_survey_instance_data_points(
            "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF8818E"
        )
        assert survey_data_points == self.test_survey_instance_data_points

    def test_single_survey_instance_data_points_fail(self, client):
        """Tests if single_survey_instance_data_points throws proper error when non-existing survey is called."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_survey_instance_data_points(
                "1FFBCDD8-2FC2-4838-B6DD-0EAE3FF88FAKE"
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_single_survey_package_instance_data_points_success(self, client):
        """Tests if single_survey_package_instance_data_points returns the proper data"""
        survey_package_data_points = client.single_survey_package_instance_data_points(
            "23B4FD48-BA41-4C9B-BAEF-D5C3DD5F8E5C"
        )
        assert survey_package_data_points == self.test_survey_package_data_points

    def test_single_survey_package_instance_data_points_fail(self, client):
        """Tests if querying a non-existent package instance throws an error"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_survey_package_instance_data_points(
                "23B4FD48-BA41-4C9B-BAEF-D5C3DD5FFAKE"
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

    # ALL DATA - RECORD SPECIFIC
    def test_all_study_data_points_record_success(self, client):
        """Tests returning data from a specific record is the right model"""
        all_data = client.all_study_data_points_record("000008")

        for data_point in all_data:
            api_keys = data_point.keys()
            assert len(self.study_data_point_model_keys) == len(api_keys)
            for key in self.study_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in study_data_point_model[key]

    def test_all_study_data_points_record_fail(self, client):
        """Tests if returning data from a non-existent records throws an error"""
        with pytest.raises(HTTPStatusError) as e:
            client.all_study_data_points_record("00FAKE")
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_all_report_data_points_record_success(self, client):
        """Tests returning data from a specific record is the right model"""
        all_data = client.all_report_data_points_record("000001")

        for data_point in all_data:
            api_keys = data_point.keys()
            assert len(self.report_data_point_model_keys) == len(api_keys)
            for key in self.report_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in report_data_point_model[key]

    def test_all_report_data_points_record_fail(self, client):
        """Tests if returning data from a non-existent records throws an error"""
        with pytest.raises(HTTPStatusError) as e:
            client.all_report_data_points_record("00FAKE")
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_all_survey_data_points_record_success(self, client):
        """Tests returning data from a specific record is the right model"""
        all_data = client.all_survey_data_points_record("000001")

        for data_point in all_data:
            api_keys = data_point.keys()
            assert len(self.survey_data_point_model_keys) == len(api_keys)
            for key in self.survey_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in survey_data_point_model[key]

    def test_all_survey_data_points_record_fail(self, client):
        """Tests if returning data from a non-existent records throws an error"""
        with pytest.raises(HTTPStatusError) as e:
            client.all_survey_data_points_record("00FAKE")
        assert "404 Client Error: Not Found for url" in str(e.value)

    # SINGLE SURVEY/REPORT - RECORD SPECIFIC
    def test_single_report_data_points_record_success(self, client):
        """Tests returning data from a specific report for a specific record is the right model"""
        report_data = client.single_report_data_points_record(
            "000001", "0D73C569-AF56-4388-88F4-BC785D9463D5"
        )

        for data_point in report_data:
            api_keys = data_point.keys()
            assert len(self.report_data_point_model_keys) == len(api_keys)
            for key in self.report_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in report_data_point_model[key]

    def test_single_report_data_points_record_fail(self, client):
        """Tests returning data from a non-existent report for a specific record throws an error"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_report_data_points_record(
                "00FAKE", "0D73C569-AF56-4388-88F4-BC785D9463D5"
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_single_survey_package_data_points_record_success(self, client):
        """Tests returning data from a specific survey package for a specific record is the right model"""
        survey_data = client.single_survey_package_data_points_record(
            "000001", "115DF660-A00A-4927-9E5F-A07D030D4A09"
        )

        for data_point in survey_data:
            api_keys = data_point.keys()
            assert len(self.survey_package_data_point_model_keys) == len(api_keys)
            for key in self.survey_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in survey_data_point_model[key]

    def test_single_survey_package_data_points_record_fail(self, client):
        """Tests returning data from a non existent survey package for a specific record throws an error"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_survey_package_data_points_record(
                "000001", "115DF660-A00A-4927-9E5F-A07D030D4FAKE"
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_single_survey_data_points_record_success(
        self,
        client,
    ):
        """Tests returning data from a specific survey for a specific record is the right model"""
        survey_data = client.single_survey_data_points_record(
            "000001", "6530D4AB-4705-4864-92AE-B0EC6200E8E5"
        )

        for data_point in survey_data:
            api_keys = data_point.keys()
            assert len(self.survey_data_point_model_keys) == len(api_keys)
            for key in self.survey_data_point_model_keys:
                assert key in api_keys
                assert type(data_point[key]) in survey_data_point_model[key]

    def test_single_survey_data_points_record_fail(self, client):
        """Tests returning data from a non existent survey for a specific record throws an error"""
        with pytest.raises(HTTPStatusError) as e:
            client.single_survey_data_points_record(
                "000001", "6530D4AB-4705-4864-92AE-B0EC6200FAKE"
            )

        assert "404 Client Error: Not Found for url" in str(e.value)

    # POST
    def test_create_study_data_points_success(self, client):
        """Tests changing data in the study"""
        fields = [
            "942A5086-88AD-44B4-A63C-85F945EAFCC7",
            "084A0536-C3E3-4088-94B0-14F1D61D61FF",
            "F0DB55D5-63F9-459D-9822-16A4BE09DB24",
            "B0312D85-D7E6-480B-8144-0B3E08726FDB",
            "D8EA7764-AF24-4A68-B14C-DB8EFDBC43FA",
        ]

        common = {"change_reason": "Testing API", "confirmed_changes": True}

        data = [
            {
                "field_id": field,
                "field_value": allowed_value(client, field),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in fields
        ]

        feedback = client.update_study_data_record("000018", common, data)
        assert feedback["total_processed"] == 5
        assert feedback["total_failed"] == 0

    def test_create_study_data_points_fail_ids(self, client):
        """Tests failing to change data in the study based on field id"""
        fields = [
            "942A5086-88AD-44B4-A63C-85F945EAFCC7",
            "084A0536-C3E3-4088-94B0-14F1D61D61FF",
            "F0DB55D5-63F9-459D-9822-16A4BE09DB24",
            "B0312D85-D7E6-480B-8144-0B3E08726FDB",
            "D8EA7764-AF24-4A68-B14C-DB8EFDBC43FA",
        ]

        common = {"change_reason": "Testing API", "confirmed_changes": True}

        data = [
            {
                "field_id": field + "FAKE",
                "field_value": allowed_value(client, field),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in fields
        ]
        feedback = client.update_study_data_record("000018", common, data)
        assert feedback["total_processed"] == 5
        assert feedback["total_failed"] == 5

    def test_create_study_data_points_fail_record(self, client):
        """Tests failing to change data in the study"""
        fields = [
            "942A5086-88AD-44B4-A63C-85F945EAFCC7",
            "084A0536-C3E3-4088-94B0-14F1D61D61FF",
            "F0DB55D5-63F9-459D-9822-16A4BE09DB24",
            "B0312D85-D7E6-480B-8144-0B3E08726FDB",
            "D8EA7764-AF24-4A68-B14C-DB8EFDBC43FA",
        ]

        common = {"change_reason": "Testing API", "confirmed_changes": True}
        data = [
            {
                "field_id": field,
                "field_value": allowed_value(client, field),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in fields
        ]

        with pytest.raises(HTTPStatusError) as e:
            client.update_study_data_record("00FAKE", common, data)
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_create_report_data_points_success(self, client):
        """Tests changing report data"""
        fields = [
            "572590BA-A1E8-4BE0-9256-F1B6842C05EB",
            "F33AD264-6483-4E7F-9E1F-CF1E2655661C",
            "4DA988EE-8D82-43D4-B6CF-02FF63EC9569",
            "FE481CDF-1F62-4542-8735-DE9DB843F0AE",
            "C6D2C69D-C126-429A-812A-21765519D23E",
        ]

        # Instantiate fake data
        common = {"change_reason": "Testing API", "confirmed_changes": True}

        data = [
            {
                "field_id": field,
                "instance_id": "D9E60041-E674-4197-819B-2C4F16E05B04",
                "field_value": allowed_value(client, field),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in fields
        ]

        # Update the report
        feedback = client.update_report_data_record(
            "000020", "D9E60041-E674-4197-819B-2C4F16E05B04", common, data
        )
        assert feedback["total_processed"] == 5
        assert feedback["total_failed"] == 0

    def test_create_report_data_points_fail_ids(self, client):
        """Tests failing to change report data based on field id"""
        fields = [
            "572590BA-A1E8-4BE0-9256-F1B6842C05EB",
            "F33AD264-6483-4E7F-9E1F-CF1E2655661C",
            "4DA988EE-8D82-43D4-B6CF-02FF63EC9569",
            "FE481CDF-1F62-4542-8735-DE9DB843F0AE",
            "C6D2C69D-C126-429A-812A-21765519D23E",
        ]

        # Instantiate fake data
        common = {"change_reason": "Testing API", "confirmed_changes": True}

        data = [
            {
                "field_id": field + "FAKE",
                "instance_id": "D9E60041-E674-4197-819B-2C4F16E05B04",
                "field_value": allowed_value(client, field),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in fields
        ]

        # Update the report
        feedback = client.update_report_data_record(
            "000020", "D9E60041-E674-4197-819B-2C4F16E05B04", common, data
        )
        assert feedback["total_processed"] == 5
        assert feedback["total_failed"] == 5

    def test_create_report_data_points_fail_record(self, client):
        """Tests failing to change report data based on record id"""
        fields = [
            "572590BA-A1E8-4BE0-9256-F1B6842C05EB",
            "F33AD264-6483-4E7F-9E1F-CF1E2655661C",
            "4DA988EE-8D82-43D4-B6CF-02FF63EC9569",
            "FE481CDF-1F62-4542-8735-DE9DB843F0AE",
            "C6D2C69D-C126-429A-812A-21765519D23E",
        ]

        # Instantiate fake data
        common = {"change_reason": "Testing API", "confirmed_changes": True}

        data = [
            {
                "field_id": field,
                "instance_id": "D9E60041-E674-4197-819B-2C4F16E05B04",
                "field_value": allowed_value(client, field),
                "change_reason": "Testing API",
                "confirmed_changes": True,
            }
            for field in fields
        ]

        # Update the report
        with pytest.raises(HTTPStatusError) as e:
            client.update_report_data_record(
                "00FAKE", "D9E60041-E674-4197-819B-2C4F16E05B04", common, data
            )
        assert "404 Client Error: Not Found for url:" in str(e.value)

    def test_create_survey_instance_data_points_success(
        self,
        client,
    ):
        """Tests changing survey data"""
        fields = [
            "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
            "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
            "5D3843C7-8341-45DD-A769-8A5D24E6CDA5",
            "6C87B052-1289-4AB2-8D4F-D15AF4DDF950",
            "A6E8C700-1A2B-4A87-AE1F-E8DC2C2F72C2",
        ]

        # Instantiate fake data
        data = [
            {
                "field_id": field,
                "instance_id": "2182E629-E0E7-4BB4-B671-CDD2C968BEFD",
                "field_value": allowed_value(client, field),
            }
            for field in fields
        ]

        # Update the survey
        feedback = client.update_survey_instance_data_record(
            "000020", "2182E629-E0E7-4BB4-B671-CDD2C968BEFD", data
        )

        assert feedback["total_processed"] == 5
        assert feedback["total_failed"] == 0

    def test_create_survey_instance_data_points_fail_ids(self, client):
        """Tests failing to change survey data based on field id"""
        fields = [
            "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
            "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
            "5D3843C7-8341-45DD-A769-8A5D24E6CDA5",
            "6C87B052-1289-4AB2-8D4F-D15AF4DDF950",
            "A6E8C700-1A2B-4A87-AE1F-E8DC2C2F72C2",
        ]

        # Instantiate fake data
        data = [
            {
                "field_id": field + "FAKE",
                "instance_id": "2182E629-E0E7-4BB4-B671-CDD2C968BEFD",
                "field_value": allowed_value(client, field),
            }
            for field in fields
        ]

        # Update the survey
        feedback = client.update_survey_instance_data_record(
            "000020", "2182E629-E0E7-4BB4-B671-CDD2C968BEFD", data
        )
        assert feedback["total_processed"] == 5
        assert feedback["total_failed"] == 5

    def test_create_survey_instance_data_points_fail_record(self, client):
        """Tests failing to change survey data based on record id"""
        fields = [
            "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
            "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
            "5D3843C7-8341-45DD-A769-8A5D24E6CDA5",
            "6C87B052-1289-4AB2-8D4F-D15AF4DDF950",
            "A6E8C700-1A2B-4A87-AE1F-E8DC2C2F72C2",
        ]

        # Instantiate fake data
        data = [
            {
                "field_id": field,
                "instance_id": "2182E629-E0E7-4BB4-B671-CDD2C968BEFD",
                "field_value": allowed_value(client, field),
            }
            for field in fields
        ]
        # Update the survey
        with pytest.raises(HTTPStatusError) as e:
            client.update_survey_instance_data_record(
                "00FAKE", "2182E629-E0E7-4BB4-B671-CDD2C968BEFD", data
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_create_survey_package_instance_data_points_success(
        self,
        client,
    ):
        """Tests changing survey package data"""
        fields = [
            "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
            "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
            "5D3843C7-8341-45DD-A769-8A5D24E6CDA5",
            "6C87B052-1289-4AB2-8D4F-D15AF4DDF950",
            "A6E8C700-1A2B-4A87-AE1F-E8DC2C2F72C2",
        ]

        # Instantiate fake data
        data = [
            {
                "field_id": field,
                "instance_id": "98BD5FCD-95B9-4B79-9A99-F37E3B6EEE22",
                "field_value": allowed_value(client, field),
            }
            for field in fields
        ]

        # Update the survey
        feedback = client.update_survey_package_instance_data_record(
            "000020", "98BD5FCD-95B9-4B79-9A99-F37E3B6EEE22", data
        )

        assert feedback["total_processed"] == 5
        assert feedback["total_failed"] == 0

    def test_create_survey_package_instance_data_points_fail_ids(self, client):
        """Tests failing to change survey package data based on field id"""
        fields = [
            "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
            "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
            "5D3843C7-8341-45DD-A769-8A5D24E6CDA5",
            "6C87B052-1289-4AB2-8D4F-D15AF4DDF950",
            "A6E8C700-1A2B-4A87-AE1F-E8DC2C2F72C2",
        ]

        # Instantiate fake data
        data = [
            {
                "field_id": field + "FAKE",
                "instance_id": "98BD5FCD-95B9-4B79-9A99-F37E3B6EEE22",
                "field_value": allowed_value(client, field),
            }
            for field in fields
        ]

        # Update the survey
        feedback = client.update_survey_package_instance_data_record(
            "000020", "98BD5FCD-95B9-4B79-9A99-F37E3B6EEE22", data
        )
        assert len(feedback["success"]) == 0
        assert len(feedback["failed"]) == 5

    def test_create_survey_package_instance_data_points_fail_records(self, client):
        """Tests failing to to change survey package data based on record id"""
        fields = [
            "FC4FAA2D-08FD-41F7-B482-444B2B6D3116",
            "ED12B07E-EDA8-4D64-8268-BE751BD5DB36",
            "5D3843C7-8341-45DD-A769-8A5D24E6CDA5",
            "6C87B052-1289-4AB2-8D4F-D15AF4DDF950",
            "A6E8C700-1A2B-4A87-AE1F-E8DC2C2F72C2",
        ]

        # Instantiate fake data
        data = [
            {
                "field_id": field,
                "instance_id": "98BD5FCD-95B9-4B79-9A99-F37E3B6EEE22",
                "field_value": allowed_value(client, field),
            }
            for field in fields
        ]

        # Update the survey
        with pytest.raises(HTTPStatusError) as e:
            client.update_survey_package_instance_data_record(
                "00FAKE", "98BD5FCD-95B9-4B79-9A99-F37E3B6EEE22", data
            )
        assert "404 Client Error: Not Found for url" in str(e.value)

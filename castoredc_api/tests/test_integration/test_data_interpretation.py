from datetime import time

import pytest


class TestDataInterpretation:
    """Tests the transformation of string values to the proper data format for analysis."""

    @pytest.fixture(scope="class")
    def integration_study_optiongroups(self, integration_study):
        integration_study.map_data()
        return integration_study

    def test_data_interpret_number(self, integration_study_optiongroups):
        # Get data point with type radio
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "1046822E-8C8B-4D8B-B29C-183CAC8B28AF", "his_smoke_dose"
        )
        # Test if answer is correct
        assert dp.value == 5

    def test_data_interpret_radio(self, integration_study_optiongroups):
        # Get data point with type radio
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "1046822E-8C8B-4D8B-B29C-183CAC8B28AF", "inc_ic"
        )
        # Test if answer is correct
        assert dp.value == "Yes"

    def test_data_interpret_dropdown(self, integration_study_optiongroups):
        # Get data point with type dropdown
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "1046822E-8C8B-4D8B-B29C-183CAC8B28AF", "pat_race"
        )
        # Test if answer is correct
        assert dp.value == "Hispanic"

    def test_data_interpret_checkbox_single(self, integration_study_optiongroups):
        # Get data point with type checkbox with a single value
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "1046822E-8C8B-4D8B-B29C-183CAC8B28AF", "ic_language"
        )
        # Test if answer is correct
        assert dp.value == "Dutch"

    def test_data_interpret_checkbox_multiple(self, integration_study_optiongroups):
        # Get data point with type checkbox with multiple values
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "1046822E-8C8B-4D8B-B29C-183CAC8B28AF", "his_family"
        )
        # Test if answer is correct
        assert dp.value == "(Cardio)myopathy|Diabetes Mellitus"

    def test_data_interpret_date(self, integration_study_optiongroups):
        # Get data point with type date
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "1046822E-8C8B-4D8B-B29C-183CAC8B28AF", "ic_date"
        )
        # Test if answer is correct
        assert dp.value == "12-05-2020"

    def test_data_interpret_year(self, integration_study_optiongroups):
        # Get data point with type year
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "1046822E-8C8B-4D8B-B29C-183CAC8B28AF", "pat_birth_year"
        )
        # Test if answer is correct
        assert dp.value == 1998

    def test_data_interpret_time(self, integration_study_optiongroups):
        # Get data point with type date time
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "A6CDB606-D094-4969-A984-7CA6E8B45883", "onset_stroke"
        )
        # Test if answer is correct
        assert dp.value == "11-05-2020 07:30:00"

    def test_data_interpret_date_time(self, integration_study_optiongroups):
        # Get data point with type date time
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "A6CDB606-D094-4969-A984-7CA6E8B45883", "onset_trombectomy"
        )
        # Test if answer is correct
        assert dp.value == time(9, 25)

    def test_data_interpret_calc(self, integration_study_optiongroups):
        # Get data point with type calc
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "A6CDB606-D094-4969-A984-7CA6E8B45883", "base_bmi"
        )
        # Test if answer is correct
        assert dp.value == 24.9

    def test_data_interpret_slider(self, integration_study_optiongroups):
        # Get data point with type slider
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "418B08AA-AED0-4BBC-895F-CD4358900E11", "VAS"
        )
        # Test if answer is correct
        assert dp.value == 58

    def test_data_interpret_text(self, integration_study_optiongroups):
        # Get data point with type string
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "1046822E-8C8B-4D8B-B29C-183CAC8B28AF", "ic_main_version"
        )
        # Test if answer is correct
        assert dp.value == "Version 2.5"

    def test_data_interpret_text_multi(self, integration_study_optiongroups):
        # Get data point with type textarea
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "67273722-1A79-46BC-9E31-B793EACEAD37", "AE_type"
        )
        # Test if answer is correct
        assert (
            dp.value
            == "Ja, nou er ging ook gewoon van alles mis en toen deed de API het opeens."
        )

    def test_data_interpret_randomization(self, integration_study_optiongroups):
        # Get data point with type randomization
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "A6CDB606-D094-4969-A984-7CA6E8B45883", "randalloc"
        )
        # Test if answer is correct
        assert dp.value == 2

    def test_data_interpret_file(self, integration_study_optiongroups):
        # Get data point with type file
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "C2318B69-A4FB-480D-960D-BC5B4E1790F6", "comorbidities"
        )
        # Test if answer is correct
        assert dp.value == "- - Uploaded file - -"

    def test_data_interpret_number_and_date(self, integration_study_optiongroups):
        # Get data point with type number and date
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "A6CDB606-D094-4969-A984-7CA6E8B45883", "fac_V_leiden"
        )
        # Test if answer is correct
        assert len(dp.value) == 2
        assert 55 in dp.value
        assert "14-01-2021" in dp.value

    def test_data_interpret_missing(self, integration_study_optiongroups):
        # Get data point with missing data
        dp = integration_study_optiongroups.get_single_data_point(
            "110014", "B153A407-8D0A-4174-B632-B89AADE3646B", "fu_sbp"
        )
        # Test if answer is correct
        assert dp.value == -98

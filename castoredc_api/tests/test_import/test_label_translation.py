import pytest

from castoredc_api.importer.helpers import read_excel, castorize_column


class TestLabelTranslation:
    """Tests the helper functions for translation of external variable labels to Castor labels."""

    @pytest.fixture(scope="class")
    def study_label_data(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_labels.xlsx"
        )
        return dataframe

    @pytest.fixture(scope="class")
    def medication_label_data(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_report_medication_labels.xlsx"
        )
        return dataframe

    @pytest.fixture(scope="class")
    def survey_label_data(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_survey_labels.xlsx"
        )
        return dataframe

    def test_record_field_success(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a record field."""
        column = study_label_data["patient"]
        import_column = castorize_column(
            to_import=column,
            new_name=["record_id"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "record_id": ["110001", "110002", "110003", "110004", "110005"]
        }

    def test_checkbox_field_success(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a checkbox field."""
        column = study_label_data["family disease history"]
        import_column = castorize_column(
            to_import=column,
            new_name=["his_family"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"his_family": ["2;3;4", "1;2", "0", "5;7", "8"]}

    def test_date_field_success(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a date field."""
        column = study_label_data["date baseline blood sample"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_bl_date"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "base_bl_date": [
                "16-03-2021",
                "17-03-2021",
                "16-03-2022",
                "17-03-2022",
                "16-03-2023",
            ]
        }

    def test_datetime_field_success(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a datetime field."""
        column = study_label_data["datetime onset stroke"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_stroke"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "onset_stroke": [
                "16-03-2021;07:30",
                "17-03-2021;15:30",
                "18-03-2022;02:00",
                "17-03-2022;21:43",
                "16-03-2023;07:22",
            ]
        }

    def test_dropdown_field_success(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a dropdown field."""
        column = study_label_data["patient race"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_race"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"pat_race": ["1", "2", "3", "4", "5"]}

    def test_numberdate_field_success(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a numberdate field."""
        column = study_label_data["factor V Leiden"]
        import_column = castorize_column(
            to_import=column,
            new_name=["fac_V_leiden"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "fac_V_leiden": [
                "55;16-03-2021",
                "33;17-03-2021",
                "-45;18-03-2022",
                "28;19-03-2022",
                "5;20-03-2023",
            ]
        }

    def test_numeric_field_success(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a number field."""
        column = study_label_data["baseline hemoglobin"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_hb"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"base_hb": ["8.3", "7.2", "9.1", "3.2", "10.3"]}

    def test_radio_field_success(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a radio field."""
        column = study_label_data["patient sex"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_sex"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"pat_sex": ["0", "0", "1", "1", "0"]}

    def test_radio_field_with_dependency_success(
        self, medication_label_data, import_study
    ):
        """Tests whether the proper format is returned when castorizing a radio field with a dependency."""
        column = medication_label_data["units"]
        import_column = castorize_column(
            to_import=column,
            new_name=["med_units", "med_other_unit"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "med_units": ["3", "7", "7", "2", "2"],
            "med_other_unit": [None, "mg/4 weeks", "mg/8 weeks", None, None],
        }

    def test_slider_field_success(self, survey_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a slider field."""
        column = survey_label_data["visual analog scale"]
        import_column = castorize_column(
            to_import=column,
            new_name=["VAS"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"VAS": ["25", "88", "13"]}

    def test_string_field_success(self, medication_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a string field."""
        column = medication_label_data["medication"]
        import_column = castorize_column(
            to_import=column,
            new_name=["med_name"],
            label_data=False,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "med_name": [
                "Azathioprine",
                "Vedolizumab",
                "Ustekinumab",
                "Thioguanine",
                "Tofacitinib",
            ]
        }

    def test_time_field_success(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a time field."""
        column = study_label_data["time onset trombectomy"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_trombectomy"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "onset_trombectomy": ["09:25", "06:33", "12:24", "23:23", "08:14"]
        }

    def test_year_field_success(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a year field."""
        column = study_label_data["year of birth"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_birth_year"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "pat_birth_year": ["1999", "1956", "1945", "1933", "1921"]
        }


class TestLabelTranslationMissing:
    """Tests the helper functions for translation of external variable labels to Castor labels with missing labels."""

    @pytest.fixture(scope="class")
    def study_label_data(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_labels_missings.xlsx"
        )
        return dataframe

    @pytest.fixture(scope="class")
    def medication_label_data(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_report_medication_labels_missings.xlsx"
        )
        return dataframe

    @pytest.fixture(scope="class")
    def survey_label_data(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_survey_labels_missings.xlsx"
        )
        return dataframe

    def test_record_field_missing(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a record field."""
        column = study_label_data["patient"]
        import_column = castorize_column(
            to_import=column,
            new_name=["record_id"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "record_id": ["110001", "110002", "110003", "110004", "110005"]
        }

    def test_checkbox_field_missing(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a checkbox field."""
        column = study_label_data["family disease history"]
        import_column = castorize_column(
            to_import=column,
            new_name=["his_family"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"his_family": [None, None, "0", "5;7", "8"]}

    def test_date_field_missing(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a date field."""
        column = study_label_data["date baseline blood sample"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_bl_date"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "base_bl_date": [
                "16-03-2021",
                "17-03-2021",
                None,
                "17-03-2022",
                "16-03-2023",
            ]
        }

    def test_datetime_field_missing(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a datetime field."""
        column = study_label_data["datetime onset stroke"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_stroke"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "onset_stroke": [
                None,
                "17-03-2021;15:30",
                "18-03-2022;02:00",
                "17-03-2022;21:43",
                "16-03-2023;07:22",
            ]
        }

    def test_dropdown_field_missing(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a dropdown field."""
        column = study_label_data["patient race"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_race"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"pat_race": ["1", "2", None, "4", "5"]}

    def test_numberdate_field_missing(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a numberdate field."""
        column = study_label_data["factor V Leiden"]
        import_column = castorize_column(
            to_import=column,
            new_name=["fac_V_leiden"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "fac_V_leiden": [
                "55;16-03-2021",
                "33;17-03-2021",
                "-45;18-03-2022",
                None,
                "5;20-03-2023",
            ]
        }

    def test_numeric_field_missing(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a number field."""
        column = study_label_data["baseline hemoglobin"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_hb"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"base_hb": ["8.3", None, "9.1", "3.2", "10.3"]}

    def test_radio_field_missing(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a radio field with missings."""
        column = study_label_data["patient sex"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_sex"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"pat_sex": ["0", "0", None, "1", "0"]}

    def test_radio_field_with_dependency_missing(
        self, medication_label_data, import_study
    ):
        """Tests whether the proper format is returned when castorizing a radio field with a dependency and missings."""
        column = medication_label_data["units"]
        import_column = castorize_column(
            to_import=column,
            new_name=["med_units", "med_other_unit"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "med_units": ["3", None, "7", "2", None],
            "med_other_unit": [None, None, "mg/8 weeks", None, None],
        }

    def test_slider_field_missing(self, survey_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a slider field with missings."""
        column = survey_label_data["visual analog scale"]
        import_column = castorize_column(
            to_import=column,
            new_name=["VAS"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"VAS": ["25", None, "13"]}

    def test_string_field_missing(self, medication_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a string field."""
        column = medication_label_data["medication"]
        import_column = castorize_column(
            to_import=column,
            new_name=["med_name"],
            label_data=False,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "med_name": ["Azathioprine", None, None, "Thioguanine", "Tofacitinib"]
        }

    def test_time_field_missing(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a time field."""
        column = study_label_data["time onset trombectomy"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_trombectomy"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "onset_trombectomy": ["09:25", "06:33", "12:24", None, "08:14"]
        }

    def test_year_field_missing(self, study_label_data, import_study):
        """Tests whether the proper format is returned when castorizing a year field."""
        column = study_label_data["year of birth"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_birth_year"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"pat_birth_year": ["1999", None, None, None, "1921"]}


class TestLabelTranslationFail:
    """Tests the helper functions for translation of erronous external variable labels to Castor labels."""

    @pytest.fixture(scope="class")
    def study_label_data_error(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_labels_errors.xlsx"
        )
        return dataframe

    @pytest.fixture(scope="class")
    def medication_label_data_error(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_report_medication_labels_errors.xlsx"
        )
        return dataframe

    @pytest.fixture(scope="class")
    def survey_label_data_error(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_survey_labels_errors.xlsx"
        )
        return dataframe

    def test_record_field_fail(self, study_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a record field."""
        column = study_label_data_error["patient"]
        import_column = castorize_column(
            to_import=column,
            new_name=["record_id"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        # Record checking fails at the import stage
        assert import_column == {"record_id": ["a", "b", "c", "d", "e"]}

    def test_checkbox_field_fail(self, study_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a checkbox field."""
        column = study_label_data_error["family disease history"]
        import_column = castorize_column(
            to_import=column,
            new_name=["his_family"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "his_family": [
                "Error;Error;Error",
                "Error",
                "Error",
                "Error;Error;Error",
                "Error",
            ]
        }

    def test_date_field_fail(self, study_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a date field."""
        column = study_label_data_error["date baseline blood sample"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_bl_date"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "base_bl_date": ["Error", "Error", "Error", "Error", "Error"]
        }

    def test_datetime_field_fail(self, study_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a datetime field."""
        column = study_label_data_error["datetime onset stroke"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_stroke"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "onset_stroke": ["Error", "Error", "Error", "Error", "Error"]
        }

    def test_dropdown_field_fail(self, study_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a dropdown field."""
        column = study_label_data_error["patient race"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_race"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "pat_race": ["Error", "Error", "Error", "Error;Error", "Error"]
        }

    def test_numberdate_field_fail(self, study_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a numberdate field."""
        column = study_label_data_error["factor V Leiden"]
        import_column = castorize_column(
            to_import=column,
            new_name=["fac_V_leiden"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "fac_V_leiden": [
                "Error",
                "33;Error",
                "Error;18-03-2022",
                "28;Error",
                "5;02-03-2023",
            ]
        }

    def test_numeric_field_fail(self, study_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a number field."""
        column = study_label_data_error["baseline hemoglobin"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_hb"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "base_hb": ["Error", "Error", "Error", "Error", "Error"]
        }

    def test_radio_field_fail(self, study_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a radio field."""
        column = study_label_data_error["patient sex"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_sex"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "pat_sex": ["Error", "Error", "Error", "Error", "Error"]
        }

    def test_radio_field_with_dependency_fail(
        self, medication_label_data_error, import_study
    ):
        """Tests whether the proper error is returned when castorizing a radio field with a dependency."""
        column = medication_label_data_error["units"]
        import_column = castorize_column(
            to_import=column,
            new_name=["med_units", "med_other_unit"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "med_units": ["7", "7", "7", "7", "7"],
            "med_other_unit": ["also", "not wrong", "because", "text", "dependency"],
        }

    def test_slider_field_fail(self, survey_label_data_error, import_study):
        """Tests whether the proper format is returned when castorizing a slider field with errors."""
        column = survey_label_data_error["visual analog scale"]
        import_column = castorize_column(
            to_import=column,
            new_name=["VAS"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"VAS": ["Error", "Error", "Error"]}

    def test_string_field_fail(self, medication_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a string field."""
        column = medication_label_data_error["medication"]
        import_column = castorize_column(
            to_import=column,
            new_name=["med_name"],
            label_data=False,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {"med_name": ["cant", "be", "wrong", "cuz", "text"]}

    def test_time_field_fail(self, study_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a time field."""
        column = study_label_data_error["time onset trombectomy"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_trombectomy"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "onset_trombectomy": ["Error", "Error", "Error", "Error", "Error"]
        }

    def test_year_field_fail(self, study_label_data_error, import_study):
        """Tests whether the proper error is returned when castorizing a year field."""
        column = study_label_data_error["year of birth"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_birth_year"],
            label_data=True,
            study=import_study,
            variable_translation=None,
        )
        assert import_column == {
            "pat_birth_year": ["Error", "Error", "Error", "Error", "Error"]
        }

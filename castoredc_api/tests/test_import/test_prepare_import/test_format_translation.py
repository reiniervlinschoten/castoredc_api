import pytest

from castoredc_api.importer.helpers import read_excel, castorize_column


class TestFormatTranslation:
    """Tests the helper functions for translation of external variable values to Castor values."""

    @pytest.fixture(scope="function")
    def study_value_data_format(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_values_format.xlsx"
        )
        return dataframe

    def test_record_field_success(self, study_value_data_format, import_study):
        """Tests whether the proper format is returned when castorizing a record field."""
        column = study_value_data_format["patient"]
        import_column = castorize_column(
            to_import=column,
            new_name=["record_id"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {
            "record_id": ["110001", "110002", "110003", "110004", "110005"]
        }

    def test_checkbox_field_success(self, study_value_data_format, import_study):
        """Tests whether the proper format is returned when castorizing a checkbox field."""
        column = study_value_data_format["family disease history"]
        import_column = castorize_column(
            to_import=column,
            new_name=["his_family"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {"his_family": ["2;3;4", "1;2", "0", "5;7", "8"]}

    def test_date_field_success(self, study_value_data_format, import_study):
        """Tests whether the proper format is returned when castorizing a date field."""
        column = study_value_data_format["date baseline blood sample"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_bl_date"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
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

    def test_datetime_field_success(self, study_value_data_format, import_study):
        """Tests whether the proper format is returned when castorizing a datetime field."""
        column = study_value_data_format["datetime onset stroke"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_stroke"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
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

    def test_dropdown_field_success(self, study_value_data_format, import_study):
        """Tests whether the proper format is returned when castorizing a dropdown field."""
        column = study_value_data_format["patient race"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_race"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {"pat_race": ["1", "2", "3", "4", "5"]}

    def test_numberdate_field_success(self, study_value_data_format, import_study):
        """Tests whether the proper format is returned when castorizing a numberdate field."""
        column = study_value_data_format["factor V Leiden"]
        import_column = castorize_column(
            to_import=column,
            new_name=["fac_V_leiden"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
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

    def test_numeric_field_success(self, study_value_data_format, import_study):
        """Tests whether the proper format is returned when castorizing a number field."""
        column = study_value_data_format["baseline hemoglobin"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_hb"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {"base_hb": ["8.3", "7.2", "9.1", "3.2", "10.3"]}

    def test_radio_field_success(self, study_value_data_format, import_study):
        """Tests whether the proper format is returned when castorizing a radio field."""
        column = study_value_data_format["patient sex"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_sex"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {"pat_sex": ["0", "0", "1", "1", "0"]}

    def test_time_field_success(self, study_value_data_format, import_study):
        """Tests whether the proper format is returned when castorizing a time field."""
        column = study_value_data_format["time onset trombectomy"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_trombectomy"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {
            "onset_trombectomy": ["09:25", "06:33", "12:24", "23:23", "08:14"]
        }

    def test_year_field_success(self, study_value_data_format, import_study):
        """Tests whether the proper format is returned when castorizing a year field."""
        column = study_value_data_format["year of birth"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_birth_year"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {
            "pat_birth_year": ["1999", "1956", "1945", "1933", "1921"]
        }


class TestFormatTranslationMissing:
    """Tests the helper functions for translation of external variable values to Castor values with missing values."""

    @pytest.fixture(scope="function")
    def study_value_data_format_missing(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_values_missings_format.xlsx"
        )
        return dataframe

    def test_record_field_missing(self, study_value_data_format_missing, import_study):
        """Tests whether the proper format is returned when castorizing a record field."""
        column = study_value_data_format_missing["patient"]
        import_column = castorize_column(
            to_import=column,
            new_name=["record_id"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {
            "record_id": ["110001", "110002", "110003", "110004", "110005"]
        }

    def test_checkbox_field_missing(
        self, study_value_data_format_missing, import_study
    ):
        """Tests whether the proper format is returned when castorizing a checkbox field."""
        column = study_value_data_format_missing["family disease history"]
        import_column = castorize_column(
            to_import=column,
            new_name=["his_family"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {"his_family": [None, None, "0", "5;7", "8"]}

    def test_date_field_missing(self, study_value_data_format_missing, import_study):
        """Tests whether the proper format is returned when castorizing a date field."""
        column = study_value_data_format_missing["date baseline blood sample"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_bl_date"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
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

    def test_datetime_field_missing(
        self, study_value_data_format_missing, import_study
    ):
        """Tests whether the proper format is returned when castorizing a datetime field."""
        column = study_value_data_format_missing["datetime onset stroke"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_stroke"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
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

    def test_dropdown_field_missing(
        self, study_value_data_format_missing, import_study
    ):
        """Tests whether the proper format is returned when castorizing a dropdown field."""
        column = study_value_data_format_missing["patient race"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_race"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {"pat_race": ["1", "2", None, "4", "5"]}

    def test_numberdate_field_missing(
        self, study_value_data_format_missing, import_study
    ):
        """Tests whether the proper format is returned when castorizing a numberdate field."""
        column = study_value_data_format_missing["factor V Leiden"]
        import_column = castorize_column(
            to_import=column,
            new_name=["fac_V_leiden"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
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

    def test_numeric_field_missing(self, study_value_data_format_missing, import_study):
        """Tests whether the proper format is returned when castorizing a number field."""
        column = study_value_data_format_missing["baseline hemoglobin"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_hb"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {"base_hb": ["8.3", None, "9.1", "3.2", "10.3"]}

    def test_radio_field_missing(self, study_value_data_format_missing, import_study):
        """Tests whether the proper format is returned when castorizing a radio field with missings."""
        column = study_value_data_format_missing["patient sex"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_sex"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {"pat_sex": ["0", "0", None, "1", "0"]}

    def test_time_field_missing(self, study_value_data_format_missing, import_study):
        """Tests whether the proper format is returned when castorizing a time field."""
        column = study_value_data_format_missing["time onset trombectomy"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_trombectomy"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {
            "onset_trombectomy": ["09:25", "06:33", "12:24", None, "08:14"]
        }

    def test_year_field_missing(self, study_value_data_format_missing, import_study):
        """Tests whether the proper format is returned when castorizing a year field."""
        column = study_value_data_format_missing["year of birth"]
        import_column = castorize_column(
            to_import=column,
            new_name=["pat_birth_year"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {"pat_birth_year": ["1999", None, None, None, "1921"]}


class TestFormatTranslationFail:
    """Tests the helper functions for translation of erronous external variable values to Castor values."""

    @pytest.fixture(scope="function")
    def study_value_data_format_error(self):
        dataframe = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_values_errors_format.xlsx"
        )
        return dataframe

    def test_date_field_fail(self, study_value_data_format_error, import_study):
        """Tests whether the proper error is returned when castorizing a date field."""
        column = study_value_data_format_error["date baseline blood sample"]
        import_column = castorize_column(
            to_import=column,
            new_name=["base_bl_date"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {
            "base_bl_date": [
                "Error: unprocessable date",
                "Error: unprocessable date",
                "Error: unprocessable date",
                "Error: unprocessable date",
                "Error: unprocessable date",
            ]
        }

    def test_datetime_field_fail(self, study_value_data_format_error, import_study):
        """Tests whether the proper error is returned when castorizing a datetime field."""
        column = study_value_data_format_error["datetime onset stroke"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_stroke"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {
            "onset_stroke": [
                "Error: unprocessable datetime",
                "Error: unprocessable datetime",
                "Error: unprocessable datetime",
                "Error: unprocessable datetime",
                "Error: unprocessable datetime",
            ]
        }

    def test_numberdate_field_fail(self, study_value_data_format_error, import_study):
        """Tests whether the proper error is returned when castorizing a numberdate field."""
        column = study_value_data_format_error["factor V Leiden"]
        import_column = castorize_column(
            to_import=column,
            new_name=["fac_V_leiden"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {
            "fac_V_leiden": [
                "55;Error: unprocessable date",
                "33;Error: unprocessable date",
                "-45;Error: unprocessable date",
                "28;Error: unprocessable date",
                "5;Error: unprocessable date",
            ]
        }

    def test_time_field_fail(self, study_value_data_format_error, import_study):
        """Tests whether the proper error is returned when castorizing a time field."""
        column = study_value_data_format_error["time onset trombectomy"]
        import_column = castorize_column(
            to_import=column,
            new_name=["onset_trombectomy"],
            label_data=False,
            study=import_study,
            variable_translation=None,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        assert import_column == {
            "onset_trombectomy": [
                "Error: unprocessable time",
                "Error: unprocessable time",
                "Error: unprocessable time",
                "Error: unprocessable time",
                "Error: unprocessable time",
            ]
        }

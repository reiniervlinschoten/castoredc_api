import pytest

from castoredc_api import CastorException
from castoredc_api.importer.import_data import import_data


class TestImportValidationErrorsSync:
    """Tests uploading data to Castor."""

    def test_import_date_error(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_error_date.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Study",
            )

        assert str(e.value) == self.study_error

    def test_import_datetime_error(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_error_datetime.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Study",
            )

        assert str(e.value) == self.study_error

    def test_import_number_error(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_error_number.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Study",
            )

        assert str(e.value) == self.study_error

    def test_import_numberdate_date_error(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_error_numberdate_date.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Study",
            )

        assert str(e.value) == self.study_error

    def test_import_numberdate_number_error(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_error_numberdate_number.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Study",
            )

        assert str(e.value) == self.study_error

    def test_import_optiongroup(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_error_optiongroup.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Study",
            )

        assert str(e.value) == self.study_error

    def test_import_time_error(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_error_time.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Study",
            )

        assert str(e.value) == self.study_error

    def test_import_year_error(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_error_year.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Study",
            )

        assert str(e.value) == self.study_error

    study_error = (
        "Non-viable data found in dataset to be imported. See output folder for details"
    )

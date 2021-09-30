import pytest

from castoredc_api import CastorException
from castoredc_api.importer.import_data import import_data


class TestImportSurvey:
    """Tests uploading data to Castor Surveys."""

    def test_import_survey_value_success(self, import_study):
        """Tests if uploading value data is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_survey_values.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
            study=import_study,
            label_data=False,
            target="Survey",
            target_name="My first survey package",
            email="python_wrapper@you-spam.com",
        )

        assert imported_data == self.survey_success

    def test_import_survey_label_success(self, import_study):
        """Tests if uploading label data is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_survey_labels.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
            study=import_study,
            label_data=True,
            target="Survey",
            target_name="My first survey package",
            email="python_wrapper@you-spam.com",
        )

        assert imported_data == self.survey_success

    def test_import_survey_value_missing(self, import_study):
        """Tests if uploading value data with missings is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_survey_values_missings.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
            study=import_study,
            label_data=False,
            target="Survey",
            target_name="My first survey package",
            email="python_wrapper@you-spam.com",
        )

        assert imported_data == self.survey_missing

    def test_import_survey_label_missing(self, import_study):
        """Tests if uploading label data with missings is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_survey_labels_missings.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
            study=import_study,
            label_data=True,
            target="Survey",
            target_name="My first survey package",
            email="python_wrapper@you-spam.com",
        )

        assert imported_data == self.survey_missing

    def test_import_survey_value_error(self, import_study):
        """Tests if uploading value data with errors is successful"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_survey_values_errors.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Survey",
                target_name="My first survey package",
                email="python_wrapper@you-spam.com",
            )

        assert str(e.value) == self.survey_error

    def test_import_survey_label_error(self, import_study):
        """Tests if uploading label data with errors is successful"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_survey_labels_errors.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
                study=import_study,
                label_data=True,
                target="Survey",
                target_name="My first survey package",
                email="python_wrapper@you-spam.com",
            )

        assert str(e.value) == self.survey_error

    def test_import_survey_error_during_upload(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_survey_values_errors_upload.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Survey",
                target_name="My first survey package",
                email="python_wrapper@you-spam.com",
            )

        assert "404 Client Error: Not Found for url:" in str(e.value)

    survey_success = {
        "110001": [
            {
                "success": {
                    "SF12_1": "3",
                    "SF12_2": "1",
                    "SF12_3": "2",
                    "SF12_12": "3",
                    "VAS": "25",
                },
                "failed": {},
            }
        ],
        "110002": [
            {
                "success": {
                    "SF12_1": "4",
                    "SF12_2": "4",
                    "SF12_3": "5",
                    "SF12_12": "6",
                    "VAS": "88",
                },
                "failed": {},
            }
        ],
        "110003": [
            {
                "success": {
                    "SF12_1": "1",
                    "SF12_2": "3",
                    "SF12_3": "4",
                    "SF12_12": "5",
                    "VAS": "13",
                },
                "failed": {},
            }
        ],
    }

    survey_missing = {
        "110001": [
            {
                "success": {"SF12_1": "3", "SF12_3": "2", "SF12_12": "3", "VAS": "25"},
                "failed": {},
            }
        ],
        "110002": [{"success": {"SF12_2": "4", "SF12_12": "6"}, "failed": {}}],
        "110003": [
            {
                "success": {"SF12_1": "1", "SF12_2": "3", "SF12_12": "5", "VAS": "13"},
                "failed": {},
            }
        ],
    }

    survey_error = (
        "Non-viable data found in dataset to be imported. See output folder for details"
    )

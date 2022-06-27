from castoredc_api.importer.helpers import read_excel, create_upload


class TestCreateUploadFormat:
    """Tests the helper functions for creation of the uploading dataframe with changed formatting options."""

    def test_create_upload_study_values_success(self, import_study):
        """Tests if creating the to_upload dataframe works for value data"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_study_values_format.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_final.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_study_values_missings(self, import_study):
        """Tests if creating the to_upload dataframe works for value data with missings"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_study_values_missings_format.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_final_missings.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_study_values_errors(self, import_study):
        """Tests if creating the to_upload dataframe works for value data with errors"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_study_values_errors_format.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
            format_options={
                "date": "%B %d %Y",
                "datetime": "%B %d %Y %I:%M %p",
                "time": "%I:%M %p",
            },
            target=None,
            target_name=None,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_final_format_errors.xlsx"
        )
        assert to_upload.equals(comparison)

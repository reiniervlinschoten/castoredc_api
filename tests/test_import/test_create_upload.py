from castoredc_api.importer.helpers import read_excel, create_upload


class TestCreateUpload:
    """Tests the helper functions for creation of the uploading dataframe."""

    def test_create_upload_study_values_success(self, import_study):
        """Tests if creating the to_upload dataframe works for value data"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_study_values.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_final.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_study_labels_success(self, import_study):
        """Tests if creating the to_upload dataframe works for label data"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_study_labels.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=True,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_final.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_study_values_missings(self, import_study):
        """Tests if creating the to_upload dataframe works for value data with missings"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_study_values_missings.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_final_missings.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_study_labels_missings(self, import_study):
        """Tests if creating the to_upload dataframe works for label data with missings"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_study_labels_missings.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=True,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_final_missings.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_study_values_errors(self, import_study):
        """Tests if creating the to_upload dataframe works for value data with errors"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_study_values_errors.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_final_errors.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_study_labels_errors(self, import_study):
        """Tests if creating the to_upload dataframe works for label data with errors"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_study_labels_errors.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=True,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_study_final_errors.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_report_medication_values_success(self, import_study):
        """Tests if creating the to_upload dataframe works for report data with dependencies"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_report_medication_values.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_report_medication_final.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_report_medication_labels_success(self, import_study):
        """Tests if creating the to_upload dataframe works for report data with dependencies"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_report_medication_labels.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=True,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_report_medication_final.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_report_medication_values_missings(self, import_study):
        """Tests if creating the to_upload dataframe works for report data with dependencies and missings"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_report_medication_values_missings.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_report_medication_final_missings.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_report_medication_labels_missings(self, import_study):
        """Tests if creating the to_upload dataframe works for report data with dependencies and missings"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_report_medication_labels_missings.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=True,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_report_medication_final_missings.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_report_medication_values_errors(self, import_study):
        """Tests if creating the to_upload dataframe works for report data with dependencies and errors"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_report_medication_values_errors.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_report_medication_final_errors.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_report_medication_labels_errors(self, import_study):
        """Tests if creating the to_upload dataframe works for report data with dependencies and errors"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_report_medication_labels_errors.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_report_medication_final_errors.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_survey_values_success(self, import_study):
        """Tests if creating the to_upload dataframe works for value data"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_survey_values.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_survey_final.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_survey_labels_success(self, import_study):
        """Tests if creating the to_upload dataframe works for label data"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_survey_labels.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=True,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_survey_final.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_survey_values_missings(self, import_study):
        """Tests if creating the to_upload dataframe works for value data with missings"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_survey_values_missings.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_survey_final_missings.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_survey_labels_missings(self, import_study):
        """Tests if creating the to_upload dataframe works for label data with missings"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_survey_labels_missings.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=True,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_survey_final_missings.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_survey_values_errors(self, import_study):
        """Tests if creating the to_upload dataframe works for value data with missings"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_survey_values_errors.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=False,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_survey_final_errors.xlsx"
        )
        assert to_upload.equals(comparison)

    def test_create_upload_survey_labels_errors(self, import_study):
        """Tests if creating the to_upload dataframe works for label data with missings"""
        to_upload = create_upload(
            path_to_upload="tests/test_import/data_files_for_import_tests/data_file_survey_labels_errors.xlsx",
            path_to_col_link="tests/test_import/link_files_for_import_tests/survey_link_file.xlsx",
            path_to_translation=None,
            path_to_merge=None,
            label_data=True,
            study=import_study,
        )
        comparison = read_excel(
            "tests/test_import/data_files_for_import_tests/data_file_survey_final_errors.xlsx"
        )
        assert to_upload.equals(comparison)

import pytest

from castoredc_api import CastorException
from castoredc_api.importer.import_data import import_data


class TestImportTranslation:
    """Tests uploading data to Castor while translating external data points."""

    def test_import_study_value_translate_success(self, import_study):
        """Tests if uploading value data is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_translate.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            study=import_study,
            label_data=False,
            target="Study",
            translation_path="tests/test_import/translate_files_for_import_tests/study_value_translate_file.xlsx",
        )

        assert imported_data == self.study_success

    def test_import_study_label_translate_success(self, import_study):
        """Tests if uploading label data is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_labels_translate.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            study=import_study,
            label_data=True,
            target="Study",
            translation_path="tests/test_import/translate_files_for_import_tests/study_label_translate_file.xlsx",
        )

        assert imported_data == self.study_success

    def test_import_study_value_translate_missing(self, import_study):
        """Tests if uploading value data with missings is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_missings_translate.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            study=import_study,
            label_data=False,
            target="Study",
            translation_path="tests/test_import/translate_files_for_import_tests/study_value_translate_file.xlsx",
        )

        assert imported_data == self.study_missing

    def test_import_study_label_translate_missing(self, import_study):
        """Tests if uploading label data with missings is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_labels_missings_translate.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
            study=import_study,
            label_data=True,
            target="Study",
            translation_path="tests/test_import/translate_files_for_import_tests/study_label_translate_file.xlsx",
        )

        assert imported_data == self.study_missing

    def test_import_study_value_translate_error(self, import_study):
        """Tests if uploading value data with errors is successful"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_values_errors_translate.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Study",
                translation_path="tests/test_import/translate_files_for_import_tests/study_value_translate_file.xlsx",
            )

        assert str(e.value) == self.study_error

    def test_import_study_label_translate_error(self, import_study):
        """Tests if uploading label data with errors is successful"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_study_labels_errors_translate.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/study_link_file.xlsx",
                study=import_study,
                label_data=True,
                target="Study",
                translation_path="tests/test_import/translate_files_for_import_tests/study_label_translate_file.xlsx",
            )

        assert str(e.value) == self.study_error

    def test_import_report_label_translation_success(self, import_study):
        """Tests if uploading label data with a translation and dependency is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_report_medication_labels_translation.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            study=import_study,
            label_data=True,
            target="Report",
            target_name="Medication",
            translation_path="tests/test_import/translate_files_for_import_tests/report_label_translate_file.xlsx",
        )

        assert imported_data == self.report_success

    study_success = {
        "110001": [
            {
                "success": {
                    "base_bl_date": "16-03-2021",
                    "base_hb": "8.3",
                    "fac_V_leiden": "55;16-03-2021",
                    "onset_stroke": "16-03-2021;07:30",
                    "onset_trombectomy": "09:25",
                    "pat_birth_year": "1999",
                    "pat_sex": "0",
                    "pat_race": "1",
                    "his_family": "2;3;4",
                },
                "failed": {},
            }
        ],
        "110002": [
            {
                "success": {
                    "base_bl_date": "17-03-2021",
                    "base_hb": "7.2",
                    "fac_V_leiden": "33;17-03-2021",
                    "onset_stroke": "17-03-2021;15:30",
                    "onset_trombectomy": "06:33",
                    "pat_birth_year": "1956",
                    "pat_sex": "0",
                    "pat_race": "2",
                    "his_family": "1;2",
                },
                "failed": {},
            }
        ],
        "110003": [
            {
                "success": {
                    "base_bl_date": "16-03-2022",
                    "base_hb": "9.1",
                    "fac_V_leiden": "-45;18-03-2022",
                    "onset_stroke": "18-03-2022;02:00",
                    "onset_trombectomy": "12:24",
                    "pat_birth_year": "1945",
                    "pat_sex": "1",
                    "pat_race": "3",
                    "his_family": "0",
                },
                "failed": {},
            }
        ],
        "110004": [
            {
                "success": {
                    "base_bl_date": "17-03-2022",
                    "base_hb": "3.2",
                    "fac_V_leiden": "28;19-03-2022",
                    "onset_stroke": "17-03-2022;21:43",
                    "onset_trombectomy": "23:23",
                    "pat_birth_year": "1933",
                    "pat_sex": "1",
                    "pat_race": "4",
                    "his_family": "5;7",
                },
                "failed": {},
            }
        ],
        "110005": [
            {
                "success": {
                    "base_bl_date": "16-03-2023",
                    "base_hb": "10.3",
                    "fac_V_leiden": "5;20-03-2023",
                    "onset_stroke": "16-03-2023;07:22",
                    "onset_trombectomy": "08:14",
                    "pat_birth_year": "1921",
                    "pat_sex": "0",
                    "pat_race": "5",
                    "his_family": "8",
                },
                "failed": {},
            }
        ],
    }

    study_missing = {
        "110001": [
            {
                "success": {
                    "base_bl_date": "16-03-2021",
                    "base_hb": "8.3",
                    "fac_V_leiden": "55;16-03-2021",
                    "onset_trombectomy": "09:25",
                    "pat_birth_year": "1999",
                    "pat_sex": "0",
                    "pat_race": "1",
                },
                "failed": {},
            }
        ],
        "110002": [
            {
                "success": {
                    "base_bl_date": "17-03-2021",
                    "fac_V_leiden": "33;17-03-2021",
                    "onset_stroke": "17-03-2021;15:30",
                    "onset_trombectomy": "06:33",
                    "pat_sex": "0",
                    "pat_race": "2",
                },
                "failed": {},
            }
        ],
        "110003": [
            {
                "success": {
                    "base_hb": "9.1",
                    "fac_V_leiden": "-45;18-03-2022",
                    "onset_stroke": "18-03-2022;02:00",
                    "onset_trombectomy": "12:24",
                    "his_family": "0",
                },
                "failed": {},
            }
        ],
        "110004": [
            {
                "success": {
                    "base_bl_date": "17-03-2022",
                    "base_hb": "3.2",
                    "onset_stroke": "17-03-2022;21:43",
                    "pat_sex": "1",
                    "pat_race": "4",
                    "his_family": "5;7",
                },
                "failed": {},
            }
        ],
        "110005": [
            {
                "success": {
                    "base_bl_date": "16-03-2023",
                    "base_hb": "10.3",
                    "fac_V_leiden": "5;20-03-2023",
                    "onset_stroke": "16-03-2023;07:22",
                    "onset_trombectomy": "08:14",
                    "pat_birth_year": "1921",
                    "pat_sex": "0",
                    "pat_race": "5",
                    "his_family": "8",
                },
                "failed": {},
            }
        ],
    }

    study_error = (
        "Non-viable data found in dataset to be imported. See output folder for details"
    )

    report_success = {
        "110001": [
            {
                "success": {
                    "med_name": "Azathioprine",
                    "med_start": "05-12-2019",
                    "med_stop": "05-12-2020",
                    "med_dose": "0.05",
                    "med_units": "3",
                },
                "failed": {},
            }
        ],
        "110002": [
            {
                "success": {
                    "med_name": "Vedolizumab",
                    "med_start": "17-08-2018",
                    "med_stop": "17-09-2020",
                    "med_dose": "300",
                    "med_units": "7",
                    "med_other_unit": "mg/4 weeks",
                },
                "failed": {},
            }
        ],
        "110003": [
            {
                "success": {
                    "med_name": "Ustekinumab",
                    "med_start": "19-12-2017",
                    "med_stop": "03-06-2019",
                    "med_dose": "90",
                    "med_units": "7",
                    "med_other_unit": "mg/8 weeks",
                },
                "failed": {},
            }
        ],
        "110004": [
            {
                "success": {
                    "med_name": "Thioguanine",
                    "med_start": "25-04-2020",
                    "med_stop": "27-05-2021",
                    "med_dose": "15",
                    "med_units": "2",
                },
                "failed": {},
            }
        ],
        "110005": [
            {
                "success": {
                    "med_name": "Tofacitinib",
                    "med_start": "01-03-2020",
                    "med_stop": "31-12-2999",
                    "med_dose": "10",
                    "med_units": "2",
                },
                "failed": {},
            }
        ],
    }

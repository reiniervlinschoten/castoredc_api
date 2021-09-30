import pytest

from castoredc_api import CastorException
from castoredc_api.importer.import_data import import_data


class TestImportReport:
    """Tests uploading data to Castor."""

    def test_import_report_value_success(self, import_study):
        """Tests if uploading value data is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_report_medication_values.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            study=import_study,
            label_data=False,
            target="Report",
            target_name="Medication",
        )

        assert imported_data == self.report_success

    def test_import_report_label_success(self, import_study):
        """Tests if uploading label data is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_report_medication_labels.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            study=import_study,
            label_data=True,
            target="Report",
            target_name="Medication",
        )

        assert imported_data == self.report_success

    def test_import_report_bulk_success(self, import_study):
        """Tests if uploading label data is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_report_medication_labels_bulk.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            study=import_study,
            label_data=True,
            target="Report",
            target_name="Medication",
        )

        assert imported_data == self.report_success_bulk

    def test_import_report_value_missing(self, import_study):
        """Tests if uploading value data with missings is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_report_medication_values_missings.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            study=import_study,
            label_data=False,
            target="Report",
            target_name="Medication",
        )

        assert imported_data == self.report_missing

    def test_import_report_label_missing(self, import_study):
        """Tests if uploading label data with missings is successful"""
        imported_data = import_data(
            data_source_path="tests/test_import/data_files_for_import_tests/data_file_report_medication_labels_missings.xlsx",
            column_link_path="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
            study=import_study,
            label_data=True,
            target="Report",
            target_name="Medication",
        )

        assert imported_data == self.report_missing

    def test_import_report_value_error(self, import_study):
        """Tests if uploading value data with errors is successful"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_report_medication_values_errors.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Report",
                target_name="Medication",
            )

        assert str(e.value) == self.report_error

    def test_import_report_label_error(self, import_study):
        """Tests if uploading label data with errors is successful"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_report_medication_labels_errors.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
                study=import_study,
                label_data=True,
                target="Report",
                target_name="Medication",
            )

        assert str(e.value) == self.report_error

    def test_import_report_error_during_upload(self, import_study):
        """Tests if uploading data with an error during the upload process fails properly"""
        with pytest.raises(CastorException) as e:
            import_data(
                data_source_path="tests/test_import/data_files_for_import_tests/data_file_report_medication_values_errors_upload.xlsx",
                column_link_path="tests/test_import/link_files_for_import_tests/report_link_file.xlsx",
                study=import_study,
                label_data=False,
                target="Report",
                target_name="Medication",
            )
        assert "404 Client Error: Not Found for url:" in str(e.value)

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

    report_missing = {
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
        "110002": [{"success": {"med_start": "17-08-2018"}, "failed": {}}],
        "110003": [
            {
                "success": {
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
            {"success": {"med_name": "Thioguanine", "med_units": "2"}, "failed": {}}
        ],
        "110005": [
            {
                "success": {
                    "med_name": "Tofacitinib",
                    "med_start": "01-03-2020",
                    "med_stop": "31-12-2999",
                    "med_dose": "10",
                },
                "failed": {},
            }
        ],
    }

    report_success_bulk = {
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
            },
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
            },
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
            },
        ],
        "110002": [
            {
                "success": {
                    "med_name": "Thioguanine",
                    "med_start": "25-04-2020",
                    "med_stop": "27-05-2021",
                    "med_dose": "15",
                    "med_units": "2",
                },
                "failed": {},
            },
            {
                "success": {
                    "med_name": "Tofacitinib",
                    "med_start": "01-03-2020",
                    "med_stop": "31-12-2999",
                    "med_dose": "10",
                    "med_units": "2",
                },
                "failed": {},
            },
        ],
    }

    report_error = (
        "Non-viable data found in dataset to be imported. See output folder for details"
    )

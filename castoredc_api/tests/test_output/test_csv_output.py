import pytest
from csv_diff import load_csv, compare

from castoredc_api.auth import auth_data
from castoredc_api.study.castor_study import CastorStudy


class TestCSVOutput:
    """Tests whether the correct data is outputted."""

    @pytest.fixture(scope="session")
    def output_data(self):
        study = CastorStudy(
            auth_data.client_id,
            auth_data.client_secret,
            auth_data.test_study_study_id,
            "data.castoredc.com",
        )
        output_data = study.export_to_csv()
        return output_data

    def test_study_export(self, output_data):
        """Tests if study export is correct."""
        diff = compare(
            load_csv(
                open(output_data["Study"]),
                key="record_id",
            ),
            load_csv(
                open("tests/test_output/data_files_for_output_tests/CastorStudy.csv"),
                key="record_id",
            ),
        )
        assert diff["added"] == []
        assert diff["removed"] == []
        assert diff["columns_added"] == []
        assert diff["columns_removed"] == []
        assert diff["changed"] == [
            {
                "key": "110001",
                "changes": {
                    "base_weight": ["88.0", "88"],
                    "base_sbp": ["120.0", "120"],
                    "base_dbp": ["65.0", "65"],
                    "base_hr": ["66.0", "66"],
                    "fac_V_leiden_number": ["55.0", "55"],
                    "base_tromboc": ["252.0", "252"],
                    "base_creat": ["88.0", "88"],
                    "fu_weight": ["66.0", "66"],
                    "fu_sbp": ["132.0", "132"],
                    "fu_dbp": ["72.0", "72"],
                    "fu_hr": ["69.0", "69"],
                    "fu_tromboc": ["366.0", "366"],
                    "fu_creat": ["99.0", "99"],
                },
            }
        ]

    @pytest.mark.xfail(
        reason="Misses Empty Surveys - Awaiting Castor Ticket", strict=True
    )
    def test_qol_survey_export(self, output_data):
        """Tests if survey export is correct."""
        diff = compare(
            load_csv(
                open(output_data["Surveys"]["QOL Survey"]),
                key="survey_instance_id",
            ),
            load_csv(
                open(
                    "tests/test_output/data_files_for_output_tests/CastorQOLSurvey.csv"
                ),
                key="survey_instance_id",
            ),
        )
        assert diff["removed"] == []
        assert diff["columns_added"] == []
        assert diff["columns_removed"] == []
        assert diff["changed"] == [
            {
                "key": "4FF130AD-274C-4C8F-A4A0-A7816A5A88E9",
                "changes": {"VAS": ["85.0", "85"]},
            }
        ]
        assert diff["added"] == []

    @pytest.mark.xfail(
        reason="Misses Empty Reports - Awaiting Castor Ticket", strict=True
    )
    def test_medication_report_export(self, output_data):
        """Tests if report export is correct."""
        diff = compare(
            load_csv(
                open(output_data["Reports"]["Medication"]),
                key="custom_name",
            ),
            load_csv(
                open(
                    "tests/test_output/data_files_for_output_tests/CastorMedication.csv"
                ),
                key="custom_name",
            ),
        )
        assert diff["removed"] == []
        assert diff["columns_added"] == []
        assert diff["columns_removed"] == []
        assert diff["changed"] == []
        assert diff["added"] == []

    def test_unscheduled_visit_report_export(self, output_data):
        """Tests if report export is correct."""
        diff = compare(
            load_csv(
                open(output_data["Reports"]["Unscheduled visit"]),
                key="custom_name",
            ),
            load_csv(
                open(
                    "tests/test_output/data_files_for_output_tests/CastorUnscheduledVisit.csv"
                ),
                key="custom_name",
            ),
        )
        assert diff["removed"] == []
        assert diff["columns_added"] == []
        assert diff["columns_removed"] == []
        assert diff["changed"] == []
        assert diff["added"] == []

    def test_comorbidities_report_export(self, output_data):
        """Tests if report export is correct."""
        diff = compare(
            load_csv(
                open(output_data["Reports"]["Comorbidities"]),
                key="custom_name",
            ),
            load_csv(
                open(
                    "tests/test_output/data_files_for_output_tests/CastorComorbidities.csv"
                ),
                key="custom_name",
            ),
        )
        assert diff["removed"] == []
        assert diff["columns_added"] == []
        assert diff["columns_removed"] == []
        assert diff["changed"] == []
        assert diff["added"] == []

    @pytest.mark.xfail(
        reason="Misses Empty Reports - Awaiting Castor Ticket", strict=True
    )
    def test_adverse_event_report_export(self, output_data):
        """Tests if report export is correct."""
        diff = compare(
            load_csv(
                open(output_data["Reports"]["Adverse event"]),
                key="custom_name",
            ),
            load_csv(
                open(
                    "tests/test_output/data_files_for_output_tests/CastorAdverseEvent.csv"
                ),
                key="custom_name",
            ),
        )
        assert diff["removed"] == []
        assert diff["columns_added"] == []
        assert diff["columns_removed"] == []
        assert diff["changed"] == []
        assert diff["added"] == []

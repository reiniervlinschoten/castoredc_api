from castoredc_api import CastorStudy
from castoredc_api.auth import auth_data


class TestSpecialCases:
    """Tests special cases of integration between CastorEDCClient and
    the CastorObjects that map the study structure and data."""

    def test_archived_report_parent(self):
        """Tries to map a study where a report is the parent of another report.
        And where an archived report is the parent of a survey."""
        study = CastorStudy(
            auth_data.client_id,
            auth_data.client_secret,
            auth_data.test_special_study_id,
            "data.castoredc.com",
        )
        study.map_data()
        # Parent is a study phase
        assert (
            study.get_single_form_instance_on_id(
                "110001", "61AD63FA-9CC9-4F4D-A58C-5FFF6D2A524F"
            ).parent
            == "Baseline"
        )
        # Parent is another report
        assert (
            study.get_single_form_instance_on_id(
                "110001", "984A9801-65F4-484F-B645-19C13FE1DF77"
            ).parent
            == "Complication - 03-01-2022 14:55:25"
        )

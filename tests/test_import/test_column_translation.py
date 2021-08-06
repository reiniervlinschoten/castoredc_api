from castoredc_api.importer.helpers import create_column_translation


class TestColumnTranslation:
    """Tests the helper functions for translation of external variable names to Castor variable names."""

    study_link = {
        "patient": ["record_id"],
        "date baseline blood sample": ["base_bl_date"],
        "baseline hemoglobin": ["base_hb"],
        "factor V Leiden": ["fac_V_leiden"],
        "datetime onset stroke": ["onset_stroke"],
        "time onset trombectomy": ["onset_trombectomy"],
        "year of birth": ["pat_birth_year"],
        "patient sex": ["pat_sex"],
        "patient race": ["pat_race"],
        "family disease history": ["his_family"],
    }

    report_link = {
        "patient": ["record_id"],
        "medication": ["med_name"],
        "startdate": ["med_start"],
        "stopdate": ["med_stop"],
        "dose": ["med_dose"],
        "units": ["med_units", "med_other_unit"],
    }

    def test_import_working_columns_base(self):
        """Tests the base case of creating a column link Dict."""
        link = create_column_translation(
            "tests/test_import/link_files_for_import_tests/study_link_file.xlsx"
        )
        assert len(link) == len(self.study_link)
        for key in self.study_link:
            assert key in link
            for value in self.study_link[key]:
                assert value in link[key]

    def test_import_working_columns_extended_dependency(self):
        """Tests the extended case of creating a column link Dict where the optiongroup option 'other' points to a free
        from text field."""
        link = create_column_translation(
            "tests/test_import/link_files_for_import_tests/report_link_file.xlsx"
        )
        assert len(link) == len(self.report_link)
        for key in self.report_link:
            assert key in link
            for value in self.report_link[key]:
                assert value in link[key]

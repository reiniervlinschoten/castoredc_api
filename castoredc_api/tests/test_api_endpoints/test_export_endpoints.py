# -*- coding: utf-8 -*-
"""
Testing class for export endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/export

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""

from castoredc_api.tests.test_api_endpoints.data_models import (
    export_data_model,
    export_structure_model,
    export_option_group_model,
)


class TestExportEndpoints:
    """Test the export endpoints of the Castor EDC API Wrapper"""

    def test_export_study_data(self, client):
        """Tests the export/data endpoint of the Castor EDC API Wrapper."""
        study_data = client.export_study_data()
        for data in study_data:
            # Assert that the number of keys between the retrieved data and the model are the same
            assert len(data.keys()) == len(export_data_model.keys())
            for key in data:
                # Assert that each retrieved key should be in the model
                assert key in export_data_model.keys()
                # Assert that the value belonging to each key is according to the model
                assert type(data[key]) in export_data_model[key]

    def test_export_study_structure(self, client):
        """Tests the export/structure endpoint of the Castor EDC API Wrapper."""
        study_structure = client.export_study_structure()
        for data in study_structure:
            # Assert that the number of keys between the retrieved data and the model are the same
            assert len(data.keys()) == len(export_structure_model.keys())
            for key in data:
                # Assert that each retrieved key should be in the model
                assert key in export_structure_model.keys()
                # Assert that the value belonging to each key is according to the model
                assert type(data[key]) in export_structure_model[key], "{}".format(key)

    def test_export_study_option_group(self, client):
        """Tests the export/optiongroups endpoint of the Castor EDC API Wrapper."""
        study_option_groups = client.export_option_groups()
        for option_group in study_option_groups:
            # Assert that the number of keys between the retrieved data and the model are the same
            assert len(option_group.keys()) == len(export_option_group_model.keys())
            for key in option_group:
                # Assert that each retrieved key should be in the model
                assert key in export_option_group_model.keys()
                # Assert that the value belonging to each key is according to the model
                assert type(option_group[key]) in export_option_group_model[key]

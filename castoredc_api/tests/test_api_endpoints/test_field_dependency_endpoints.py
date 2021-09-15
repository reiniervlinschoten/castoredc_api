# -*- coding: utf-8 -*-
"""
Testing class for field-dependency endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/field-dependency

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import field_dep_model
from castoredc_api import CastorException


class TestFieldDependency:
    model_keys = field_dep_model.keys()

    test_field_dep = {
        "id": "9",
        "operator": "==",
        "value": "1",
        "parent_id": "BA93857C-1EBB-4DFF-92F3-EEE92D944686",
        "child_id": "CF86C999-256F-49D6-8D59-90D2A8B9A3D8",
        "_links": {
            "self": {
                "href": "https://data.castoredc.com/api/study/D234215B-D956-482D"
                "-BF17-71F2BB12A2FD/field-dependency/9"
            }
        },
    }

    @pytest.fixture(scope="class")
    def all_field_dependencies(self, client):
        """Get all field dependencies from the Castor database."""
        all_field_dependencies = client.all_field_dependencies()
        return all_field_dependencies

    def test_all_field_dependencies(self, all_field_dependencies, item_totals):
        """Test whether all field dependencies are returned."""
        # Test whether there are any field dependencies.
        assert (
            len(all_field_dependencies) > 0
        ), "No field dependencies found, is this right?"
        assert len(all_field_dependencies) == item_totals("/field-dependency")

    def test_all_field_dependencies_model(self, all_field_dependencies):
        """Tests the model of the field dependencies returned by all_field_dependencies."""
        # Loop over the dependencies
        for dependency in all_field_dependencies:
            api_keys = dependency.keys()
            # Check if the number of keys is the same between the model and the API
            assert len(self.model_keys) == len(api_keys)
            # Check of the keys and types of values are the same between the model and the API
            for key in self.model_keys:
                assert key in api_keys
                assert type(dependency[key]) in field_dep_model[key]

    def test_all_field_dependencies_data(self, all_field_dependencies):
        """Tests the data of the field dependencies returned by all_field_dependencies."""
        # Select one dependency
        field_dependency = all_field_dependencies[4]
        # Tests whether the proper dependency is returned
        assert field_dependency == self.test_field_dep

    def test_single_field_success(self, client):
        """Tests if single field dependency returns the proper data."""
        field_dependency = client.single_field_dependency(9)
        assert field_dependency == self.test_field_dep

    def test_single_field_failure(self, client):
        """Tests whether a wrong id throws an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_field_dependency(2)
        assert "404 Client Error: Not Found for url" in str(e.value)

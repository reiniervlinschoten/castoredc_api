# -*- coding: utf-8 -*-
"""
Testing class for country endpoints of the Castor EDC API Wrapper.
Link: https://data.castoredc.com/api#/country

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""
import pytest
from httpx import HTTPStatusError

from castoredc_api.tests.test_api_endpoints.data_models import (
    country_model,
    single_country_model,
)
from castoredc_api import CastorException


class TestCountry:
    model_keys = country_model.keys()
    single_country_model_keys = single_country_model.keys()

    @pytest.fixture(scope="class")
    def all_countries(self, client):
        """Returns a list of dicts containing all countries in the Castor database."""
        all_countries = client.all_countries()
        return all_countries

    def test_all_countries(self, all_countries):
        """Tests if the all_countries function returns all countries."""
        countries = [container["country_name"] for container in all_countries]
        assert len(countries) == 250
        assert "Netherlands" in countries
        assert "Maldives" in countries

    def test_all_countries_model(self, all_countries):
        """Tests if the value returned by the all_countries function is equal to the specified country model."""
        # Select a country
        country = all_countries[167]
        api_keys = country.keys()

        # Test if the the number of keys is equal between the API and the model
        assert len(api_keys) == len(self.model_keys)

        # Test if the keys are the same, and the value is of the specified type
        for key in api_keys:
            assert key in self.model_keys
            assert type(country[key]) in country_model[key]

    def test_all_countries_data(self, all_countries):
        """Tests if all_countries returns the proper data."""
        # Select a country
        country = all_countries[167]

        # Test if the values are as they should be
        assert country["id"] == "169"
        assert country["country_id"] == "169"
        assert country["country_name"] == "Netherlands"
        assert country["country_tld"] == ".nl"
        assert country["country_cca2"] == "NL"
        assert country["country_cca3"] == "NLD"

    def test_single_country_success(self, client):
        """Tests if the single_country function returns a proper country model."""
        # Get a country
        country = client.single_country("169")
        api_keys = country.keys()

        # Test if the the number of keys is equal between the API and the model
        assert len(api_keys) == len(self.single_country_model_keys)

        # Test if the keys are the same, and the value is of the specified type
        for key in api_keys:
            assert key in self.single_country_model_keys
            assert type(country[key]) in single_country_model[key], "{}".format(country)

        # Test if the values are as they should be
        assert country["id"] == 169
        assert country["country_id"] == 169
        assert country["country_name"] == "Netherlands"
        assert country["country_tld"] == ".nl"
        assert country["country_cca2"] == "NL"
        assert country["country_cca3"] == "NLD"

    def test_single_country_failure_too_large(self, client):
        """Tests if retrieving a non-existent (edge case: upper range) country ID raises an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_country(252)
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_single_country_failure_negative(self, client):
        """Tests if retrieving a non-existent (edge case: negative) country ID raises an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_country(-1)
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_single_country_failure_zero(self, client):
        """Tests if retrieving a non-existent (edge case: zero) country ID raises an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_country(0)
        assert "404 Client Error: Not Found for url" in str(e.value)

    def test_single_country_failure_one(self, client):
        """Tests if retrieving a non-existent (edge case: lower range) country ID raises an error."""
        with pytest.raises(HTTPStatusError) as e:
            client.single_country(1)
        assert "404 Client Error: Not Found for url" in str(e.value)

# -*- coding: utf-8 -*-
"""
Global fixtures for testing CastorStudy

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""

pytest_plugins = [
    "castoredc_api.tests.test_castor_objects.fixtures_castor_objects",
    "castoredc_api.tests.test_integration.fixtures_integration",
    "castoredc_api.tests.test_api_endpoints.fixtures_api",
    "castoredc_api.tests.test_import.fixtures_import",
]

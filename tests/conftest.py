# -*- coding: utf-8 -*-
"""
Global fixtures for testing CastorStudy

@author: R.C.A. van Linschoten
https://orcid.org/0000-0003-3052-596X
"""

pytest_plugins = [
    "tests.test_castor_objects.fixtures_castor_objects",
    "tests.test_integration.fixtures_integration",
    "tests.test_api_endpoints.fixtures_api",
    "tests.test_import.fixtures_import",
]
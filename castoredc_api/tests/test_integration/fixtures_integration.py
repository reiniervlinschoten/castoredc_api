import pytest

from castoredc_api.auth import auth_data
from castoredc_api.study.castor_study import CastorStudy


@pytest.fixture(scope="class")
def integration_study():
    study = CastorStudy(
        auth_data.client_id,
        auth_data.client_secret,
        auth_data.test_client_study_id,
        "data.castoredc.com",
    )
    return study


@pytest.fixture(scope="class")
def integration_study_format():
    study = CastorStudy(
        auth_data.client_id,
        auth_data.client_secret,
        auth_data.test_client_study_id,
        "data.castoredc.com",
        format_options={
            "date": "%B %e %Y",
            "datetime": "%B %e %Y %I:%M %p",
            "time": "%I:%M %p",
        }
    )
    return study

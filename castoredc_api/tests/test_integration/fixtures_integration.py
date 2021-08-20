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

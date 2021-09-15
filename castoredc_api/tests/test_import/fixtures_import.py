import pytest

from castoredc_api.study.castor_study import CastorStudy
from castoredc_api.auth import auth_data


@pytest.fixture(scope="session")
def import_study():
    study = CastorStudy(
        auth_data.client_id,
        auth_data.client_secret,
        auth_data.test_import_study_id,
        "data.castoredc.com",
    )
    study.map_structure()
    return study

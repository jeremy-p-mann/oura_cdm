import pytest

from oura_cdm.extract_oura import get_oura_data
from oura_cdm.pipeline import run


@pytest.fixture(scope='session')
def start_date():
    return '2022-01-17'


@pytest.fixture(scope='session')
def end_date():
    return '2022-02-02'


@pytest.fixture(scope='session')
def oura_data(start_date, end_date):
    return get_oura_data(start_date=start_date, end_date=end_date)


@pytest.fixture(scope='session')
def pipeline_inputs():
    return {
        "target_folder_name": "sleep_data_test"
    }


@pytest.fixture(scope='session')
def pipeline_artifacts(pipeline_inputs):
    return run(**pipeline_inputs)


@pytest.fixture(scope='session')
def target_folder_name():
    return 'sleep_data_test'

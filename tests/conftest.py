import pytest

from oura_cdm.extract_oura import get_oura_data


@pytest.fixture(scope='session')
def start_date():
    return '2022-01-17'


@pytest.fixture(scope='session')
def end_date():
    return '2022-02-02'


@pytest.fixture(scope='session')
def oura_data(start_date, end_date):
    return get_oura_data(start_date=start_date, end_date=end_date)

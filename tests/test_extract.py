import pytest


@pytest.fixture(scope='session')
def observation_dates(oura_data):
    return [
        observations['summary_date']
        for observations in oura_data
    ]


def test_oura_data_keys(oura_data):
    assert {"light", "rem", "deep"}.issubset(set(oura_data[0].keys()))


def test_start_date(observation_dates, start_date):
    for date in observation_dates:
        assert start_date <= date


def test_end_date(observation_dates, end_date):
    for date in observation_dates:
        assert end_date >= date

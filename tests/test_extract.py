import os

import pytest

from oura_cdm.extract_oura import get_oura_data


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


@pytest.fixture(params=['asdfjkl'])
def invalid_token_env(request, monkeypatch):
    token = request.param
    if token is not None:
        monkeypatch.setenv('OURA_TOKEN', token)
    yield token


def test_all_env_variables(invalid_token_env):
    data = get_oura_data(start_date='2022-01-17', end_date='2022-02-02')
    if invalid_token_env is not None:
        assert os.environ['OURA_TOKEN'] == invalid_token_env
        assert len(data) == 0

import pytest

from oura_cdm.extract_oura import get_oura_data


@pytest.fixture
def oura_data():
    return get_oura_data()

@pytest.mark.requires_access
def test_oura_data_keys(oura_data):
    assert {"light", "rem", "deep"}.issubset(set(oura_data[0].keys()))

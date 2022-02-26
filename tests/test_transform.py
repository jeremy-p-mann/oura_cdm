import pytest

from oura_cdm.concepts import SleepConcept
from oura_cdm.observation import get_observation_table
from oura_cdm.schemas import SleepObservationSchema


@pytest.fixture
def observation_df(oura_data):
    observation_df = get_observation_table(oura_data)
    return observation_df


def test_observation_table_schema(observation_df):
    SleepObservationSchema.validate(observation_df)


def test_n_observations(oura_data, observation_df):
    n_sleep_concepts = len(SleepConcept)
    assert len(observation_df) == n_sleep_concepts * len(oura_data)

import pytest

from oura_cdm.concepts import SleepConcept, OuraKeywords
from oura_cdm.observation import get_observation_table
from oura_cdm.schemas import SleepObservationSchema


@pytest.fixture
def observation_df(oura_data):
    observation_df = get_observation_table(oura_data)
    return observation_df


@pytest.fixture
def raw_observation(oura_data):
    return oura_data[0]


@pytest.fixture
def raw_observation_date(raw_observation):
    return raw_observation[OuraKeywords.DATE]


@pytest.fixture(params=list(SleepConcept))
def concept(request,):
    return request.param


def test_observation_table_schema(observation_df):
    SleepObservationSchema.validate(observation_df)


def test_n_observations(oura_data, observation_df):
    n_sleep_concepts = len(SleepConcept)
    assert len(observation_df) == n_sleep_concepts * len(oura_data)


def test_observation_date(raw_observation_date, observation_df):
    observation_dates = list(observation_df.observation_date)
    assert raw_observation_date in observation_dates


def test_observation_rem(
    raw_observation_date, raw_observation, observation_df,
    concept
):
    actual = raw_observation[OuraKeywords.get_keyword_from_concept(concept)]
    expected_ids = observation_df[
        (observation_df.observation_date == raw_observation_date)
        * (observation_df.observation_concept_id == concept)
    ].observation_id
    assert len(expected_ids) == 1
    # import pdb; pdb.set_trace()
    # expected = observation_df.value_as_number[expected_ids.iloc[0]]

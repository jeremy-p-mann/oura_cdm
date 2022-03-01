import pandas as pd
import pytest

from oura_cdm.concepts import ObservationConcept, OuraKeywords
from oura_cdm.journey import make_observation_journey_df
from oura_cdm.schemas import make_journey_schema


@pytest.fixture(scope='session')
def journey_df(observation_df):
    return make_observation_journey_df(observation_df)


@pytest.fixture(scope='session')
def journey_schema(observation_df):
    return make_journey_schema(observation_df)


def test_observations_columns_in_observation_journey(journey_df):
    concept_ids = {c.value for c in ObservationConcept}
    assert set(journey_df.columns) == concept_ids


def test_n_journeys(journey_df, oura_data):
    assert len(journey_df) == len(oura_data)


def test_observation_value_at_date(
        observation_concept, journey_df, raw_observation):
    date = raw_observation['summary_date']
    expected_value = raw_observation[
        OuraKeywords.get_keyword_from_concept(observation_concept)
    ]
    expected = expected_value \
        * ObservationConcept.get_reference_value(observation_concept)
    actual = journey_df.loc[date, observation_concept.value]
    assert expected == actual


def test_journey_index_datetime(journey_df):
    assert isinstance(journey_df.index, pd.DatetimeIndex)


def test_journey_fits_schema(journey_df, journey_schema):
    journey_schema.validate(journey_df)

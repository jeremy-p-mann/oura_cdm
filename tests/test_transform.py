import pytest

from oura_cdm.concepts import (ObservationConcept, ObservationTypeConcept,
                               OuraKeywords, OuraConcept)
from oura_cdm.observation import get_observation_table
from oura_cdm.schemas import ObservationSchema


@pytest.fixture
def raw_observation_value(raw_observation, observation_concept):
    return raw_observation[OuraConcept.get_keyword_from_concept(observation_concept)]


@pytest.fixture
def raw_observation_date(raw_observation):
    return raw_observation[OuraConcept.SUMMARY_DATE.concept_name]


@pytest.fixture(params=list(ObservationConcept))
def observation_concept(request,):
    return request.param


@pytest.fixture
def observation_dict(observation_concept, observation_df, raw_observation_date):
    expecteds = observation_df[
        (observation_df.observation_date == raw_observation_date)
        * (observation_df.observation_concept_id == observation_concept)
    ]
    assert len(expecteds) == 1
    return dict(expecteds.iloc[0, :])


def test_observation_table_schema(observation_df):
    ObservationSchema.validate(observation_df)


def test_n_observations(oura_data, observation_df):
    assert len(observation_df) == len(ObservationConcept) * len(oura_data)


def test_observation_date(raw_observation_date, observation_df):
    observation_dates = list(observation_df.observation_date)
    assert raw_observation_date in observation_dates


def test_observation_values(observation_dict, raw_observation_value):
    assert float(raw_observation_value) == observation_dict['value_as_number']


def test_source_value(observation_dict, raw_observation_value):
    expected = observation_dict['value_source_value']
    try:
        expected = int(expected)
    except ValueError:
        pass
    assert raw_observation_value == expected


def test_units(observation_dict, observation_concept):
    unit_id = observation_dict['unit_concept_id']
    assert unit_id == ObservationConcept.get_unit_source_id(
        observation_concept)


def test_observation_type_is_valid(observation_dict):
    type_id = observation_dict['observation_type_concept_id']
    assert type_id in {c.value for c in ObservationTypeConcept}


def test_no_entries_to_calculuate(oura_data):
    observation_df = get_observation_table(oura_data[:0])
    assert len(observation_df) == 0


@pytest.mark.skip
def test_observation_datetime(
        observation_dict
):
    assert False

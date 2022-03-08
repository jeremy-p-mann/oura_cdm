import pytest

from oura_cdm.concepts import (ObservationConcept, ObservationTypeConcept,
                               OuraConcept)
from oura_cdm.observation import get_observation_table
from oura_cdm.schemas import ObservationSchema


@pytest.fixture
def raw_observation_value(raw_observation, observation_concept, ontology):
    oura_concept = ontology.mapped_from(observation_concept)
    keyword = ontology.get_concept_code(oura_concept)
    return raw_observation[keyword]


@pytest.fixture
def raw_observation_date(raw_observation, ontology):
    keyword = ontology.get_concept_code(OuraConcept.SUMMARY_DATE)
    return raw_observation[keyword]


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


def test_units(observation_dict, observation_concept, ontology):
    unit_id = observation_dict['unit_concept_id']
    oura_concept = ontology.mapped_from(observation_concept)
    unit = ontology.get_unit(oura_concept)
    assert unit_id == unit.value


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

import pytest

from oura_cdm.concepts import (Concept, ObservationConcept,
                               ObservationTypeConcept, UnitConcept)


@pytest.fixture(params=Concept.get_all_concepts())
def concept(request):
    return request.param


@pytest.fixture(params=[c for c in UnitConcept])
def unit_concept(request):
    return request.param


@pytest.fixture(params=[c for c in ObservationTypeConcept])
def observation_type_concept(request):
    return request.param


def test_rem_sleep_name(ontology):
    rem_name = ontology.get_concept_name(
        ObservationConcept.REM_SLEEP_DURATION)
    assert rem_name == 'REM sleep duration'


def test_units_are_units(ontology, unit_concept):
    domain_id = ontology.get_domain_id(unit_concept)
    assert domain_id == UnitConcept.get_domain_id()


def test_observation_concepts_are_concepts(ontology, observation_concept):
    domain_id = ontology.get_domain_id(observation_concept)
    assert domain_id == ObservationConcept.get_domain_id()


def test_observation_type_domain(ontology, observation_type_concept):
    domain_id = ontology.get_domain_id(observation_type_concept)
    assert domain_id == ObservationTypeConcept.get_domain_id()


def test_concepts_in_concept_df(ontology, concept):
    assert ontology.is_valid(concept)

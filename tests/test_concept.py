import pytest

from oura_cdm.concepts import (ObservationConcept, ObservationTypeConcept,
                               UnitConcept,)
from oura_cdm.ontology import Ontology


@pytest.fixture(scope='session')
def ontology():
    return Ontology()


@pytest.fixture(params=[c for c in UnitConcept])
def unit_concept_id(request):
    return request.param.value


@pytest.fixture(params=[c for c in ObservationConcept])
def observation_concept_id(request):
    return request.param.value


@pytest.fixture(params=[c for c in ObservationTypeConcept])
def observation_type_concept_id(request):
    return request.param.value


def test_rem_sleep_name(ontology):
    rem_name = ontology.get_concept_name(
        ObservationConcept.REM_SLEEP_DURATION.value)
    assert rem_name == 'REM sleep duration'


def test_units_are_units(ontology, unit_concept_id):
    domain_id = ontology.get_domain_id(unit_concept_id)
    assert domain_id == UnitConcept.get_domain_id()


def test_observation_concepts_are_concepts(ontology, observation_concept_id):
    domain_id = ontology.get_domain_id(observation_concept_id)
    assert domain_id == ObservationConcept.get_domain_id()


def test_observation_type_domain(ontology, observation_type_concept_id):
    domain_id = ontology.get_domain_id(observation_type_concept_id)
    assert domain_id == ObservationTypeConcept.get_domain_id()

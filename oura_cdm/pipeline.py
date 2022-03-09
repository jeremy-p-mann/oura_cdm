from functools import partial
from typing import Any, Dict

from oura_cdm.artifacts import Artifact
from oura_cdm.concepts import get_ontology_dfs
from oura_cdm.extract_oura import get_oura_data
from oura_cdm.journey import make_observation_journey_df
from oura_cdm.logs import log_info
from oura_cdm.observation import get_observation_table
from oura_cdm.schemas import (ConceptRelationshipSchema, ConceptSchema,
                              ObservationSchema, make_journey_schema)

log_info_p = partial(log_info, **{'name': __name__})


def validate_run(artifacts: Dict[str, Any]):
    log_info_p('Validating Observation Data')
    for artifact in Artifact:
        assert artifact in artifacts.keys()
    # TODO this should all live in the artifacts class
    observation_df = artifacts[Artifact.OBSERVATION]
    ObservationSchema.validate(observation_df)

    journey_df = artifacts[Artifact.JOURNEY]
    journey_schema = make_journey_schema(observation_df)
    journey_schema.validate(journey_df)

    concept_df = artifacts[Artifact.CONCEPT]
    concept_relationship_df = artifacts[Artifact.CONCEPT_RELATIONSHIP]
    ConceptSchema.validate(concept_df)
    ConceptRelationshipSchema.validate(concept_relationship_df)

    log_info_p('Observation data valid')


def run(**kwargs):
    log_info_p('Beginning Run')
    raw_oura_data = get_oura_data()
    observation_df = get_observation_table(raw_oura_data)
    journey_df = make_observation_journey_df(observation_df)
    concept_df, concept_relationship_df = get_ontology_dfs()
    artifacts: Dict[str, Any] = {
        Artifact.OBSERVATION: observation_df,
        Artifact.SOURCE_DATA: raw_oura_data,
        Artifact.JOURNEY: journey_df,
        Artifact.CONCEPT: concept_df,
        Artifact.CONCEPT_RELATIONSHIP: concept_relationship_df,
    }
    log_info_p('Run Successful')
    return artifacts

from functools import partial
from typing import Any, Dict

from oura_cdm.extract_oura import get_oura_data
from oura_cdm.logs import log_info
from oura_cdm.observation import get_observation_table
from oura_cdm.schemas import ObservationSchema, make_journey_schema
from oura_cdm.journey import make_observation_journey_df
from oura_cdm.artifacts import Artifact

log_info_p = partial(log_info, **{'name': __name__})


def validate_run(artifacts: Dict[str, Any]):
    log_info_p('Validating Observation Data')
    for artifact in Artifact:
        assert artifact.value in artifacts.keys()
    observation_df = artifacts[Artifact.OBSERVATION.value]
    ObservationSchema.validate(observation_df)

    journey_df = artifacts[Artifact.JOURNEY.value]
    journey_schema = make_journey_schema(observation_df)
    journey_schema.validate(journey_df)

    log_info_p('Observation data valid')


def run(target_folder_name: str):
    # TODO This doesn't need target folder why is it here
    log_info_p('Beginning Run')
    raw_oura_data = get_oura_data()
    observation_df = get_observation_table(raw_oura_data)
    journey_df = make_observation_journey_df(observation_df)
    artifacts: Dict[str, Any] = {
        Artifact.OBSERVATION.value: observation_df,
        Artifact.SOURCE_DATA.value: raw_oura_data,
        Artifact.JOURNEY.value: journey_df,
    }
    log_info_p('Run Successful')
    return artifacts

import json
import os
from functools import partial
from typing import Any, Dict

from oura_cdm.artifacts import Artifact
from oura_cdm.logs import log_info, log_warning

log_info_p = partial(log_info, **{'name': __name__})
log_warning_p = partial(log_warning, **{'name': __name__})


CSV_SEP = '\t'

def write_artifacts(artifacts: Dict[str, Any], target_folder_name: str):
    log_info_p('Writing artifacts')
    os.makedirs(target_folder_name, mode=0o777,)
    observation_table_filename = Artifact.get_filename(Artifact.OBSERVATION)
    observation_table_filepath = \
        f'{target_folder_name}/{observation_table_filename}'
    source_data_filename = Artifact.get_filename(Artifact.SOURCE_DATA)
    source_data_filepath = \
        f'{target_folder_name}/{source_data_filename}'
    journey_filename = Artifact.get_filename(Artifact.JOURNEY)
    journey_filepath = \
        f'{target_folder_name}/{journey_filename}'
    concept_data_filename = Artifact.get_filename(Artifact.CONCEPT)
    cr_data_filename = Artifact.get_filename(Artifact.CONCEPT_RELATIONSHIP)
    concept_data_filepath = \
        f'{target_folder_name}/{concept_data_filename}'
    concept_relationship_data_filepath = \
        f'{target_folder_name}/{cr_data_filename}'

    log_info_p('Writing observation table')
    artifacts[Artifact.OBSERVATION].to_csv(
        observation_table_filepath,
        sep=CSV_SEP
    )
    log_info_p(f'Observation table written to {observation_table_filepath}')
    log_info_p('Writing journey table')
    artifacts[Artifact.JOURNEY].to_csv(
        journey_filepath,
        sep=CSV_SEP
    )
    log_info_p(f'Journey table written to {journey_filepath}')
    log_info_p('Writing Source Data')
    with open(source_data_filepath, 'w') as f:
        json.dump(artifacts[Artifact.SOURCE_DATA], f)
    log_info_p(f'Source data written to {source_data_filepath}')

    log_info_p('Writing Concept Data')
    artifacts[Artifact.CONCEPT].to_csv(
        concept_data_filepath,
        sep=CSV_SEP
    )
    log_info_p(f'Concept data written to {concept_data_filepath}')
    log_info_p('Writing Concept Relationship Data')
    artifacts[Artifact.CONCEPT_RELATIONSHIP].to_csv(
        concept_relationship_data_filepath,
        sep=CSV_SEP
    )
    log_info_p(f'Concept Relationship data written to {concept_relationship_data_filepath}')
    log_info_p(
        f'Artifacts Successfully written to folder {target_folder_name}')


def clean_up_run(
    target_folder_name: str
):
    log_info_p('Cleaning Run')
    if target_folder_name not in os.listdir():
        log_warning_p(f'{target_folder_name} not present, nothing to clean')
        return None
    for file in os.listdir(target_folder_name):
        os.remove(f'{target_folder_name}/{file}')
    os.rmdir(target_folder_name)
    log_info_p(f'Run cleaned, {target_folder_name} removed')

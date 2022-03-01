import os
from functools import partial
from typing import Any, Dict

from oura_cdm.extract_oura import get_oura_data
from oura_cdm.logs import log_info
from oura_cdm.observation import get_observation_table
from oura_cdm.schemas import ObservationSchema

log_info_p = partial(log_info, **{'name': __name__})


def validate_run(artifacts: Dict[str, Any]):
    log_info_p('Validating Observation Data')
    ObservationSchema.validate(artifacts['observation_df'])
    log_info_p('Observation data valid')


def run(target_folder_name: str):
    # TODO This doesn't need target folder why is it here
    log_info_p('Beginning Run')
    raw_oura_data = get_oura_data()
    observation_df = get_observation_table(raw_oura_data)
    artifacts: Dict[str, Any] = {
        "observation_df": observation_df
    }
    log_info_p('Run Successful')
    return artifacts


def write_artifacts(artifacts: Dict[str, Any], target_folder_name: str):
    log_info_p('Writing artifacts')
    os.makedirs(target_folder_name, mode=0o777,)
    observation_table_filepath = f'{target_folder_name}/observation.csv'
    log_info_p('Writing observation table')
    artifacts['observation_df'].to_csv(
        observation_table_filepath,
        sep='\t'
    )
    log_info_p(f'Observation table written to {observation_table_filepath}')
    log_info_p(
        f'Artifacts Successfully written to folder {target_folder_name}')


def clean_up_run(
    target_folder_name: str
):
    log_info_p('Cleaning Run')
    for file in os.listdir(target_folder_name):
        os.remove(f'{target_folder_name}/{file}')
    os.rmdir(target_folder_name)
    log_info_p(f'Run cleaned, {target_folder_name} removed')

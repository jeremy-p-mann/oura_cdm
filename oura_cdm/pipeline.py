import os
from typing import Any, Dict

import pandas as pd

from oura_cdm.extract_oura import get_oura_data
from oura_cdm.observation import get_observation_table
from oura_cdm.schemas import SleepObservationSchema


def validate_run(artifacts: Dict[str, Any]):
    SleepObservationSchema.validate(artifacts['observation_df'])


def run(
    target_folder_name: str
):
    raw_oura_data = get_oura_data()
    observation_df = get_observation_table(raw_oura_data)
    artifacts: Dict[str, Any] = {
        "observation_df": observation_df
    }
    return artifacts


def write_artifacts(artifacts: Dict[str, Any], target_folder_name: str):
    os.makedirs(target_folder_name, mode=0o777,)
    artifacts['observation_df'].to_csv(
        f'{target_folder_name}/observation.csv',
        sep='\t'
    )


def clean_up_run(
    target_folder_name: str
):
    for file in os.listdir(target_folder_name):
        os.remove(f'{target_folder_name}/{file}')
    os.rmdir(target_folder_name)

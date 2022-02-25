import os
from typing import Dict, Any


def validate_run(artifacts: Dict[str, Any]):
    pass


def run(
    target_folder_name: str
):
    artifacts: Dict[str, Any] = {}
    return artifacts


def write_artifacts(artifacts: Dict[str, Any], target_folder_name: str):
    os.makedirs(target_folder_name, mode=0o777,)


def clean_up_run(
    target_folder_name: str
):
    os.rmdir(target_folder_name)

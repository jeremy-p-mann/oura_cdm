import os

import pytest

from oura_cdm.write import clean_up_run
from oura_cdm.artifacts import Artifact


@pytest.fixture(scope='session')
def etl_process(target_folder_name):
    if target_folder_name in os.listdir():
        clean_up_run(target_folder_name)
    status = os.system(f'python3 oura_cdm/main.py {target_folder_name}')
    yield status
    clean_up_run(target_folder_name)


def test_cli_creates_folder(etl_process, target_folder_name):
    assert target_folder_name in os.listdir()


def test_cli_exit_status(etl_process):
    assert etl_process == 0


def test_artifacts_written(etl_process, target_folder_name):
    assert {Artifact.get_filename(a) for a in Artifact} == \
        set(os.listdir(target_folder_name))

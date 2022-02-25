import os

import pytest

from oura_cdm.pipeline import clean_up_run


@pytest.fixture()
def target_folder_name():
    return 'sleep_data_test'


@pytest.fixture()
def etl_process(target_folder_name):
    if target_folder_name in os.listdir():
        clean_up_run(target_folder_name)
    status = os.system(f'python3 oura_cdm/main.py {target_folder_name}')
    print(os.listdir())
    yield status
    clean_up_run(target_folder_name)


def test_cli_creates_folder(etl_process, target_folder_name):
    assert target_folder_name in os.listdir()


def test_cli_exit_status(etl_process):
    assert etl_process == 0


def test_observation_table_exists(etl_process, target_folder_name):
    assert "observation.csv" in os.listdir(target_folder_name)

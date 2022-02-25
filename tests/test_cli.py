import os

import pytest


@pytest.yield_fixture()
def target_folder_name():
    return 'sleep_data_test'


@pytest.yield_fixture()
def etl_process(target_folder_name):
    if target_folder_name in os.listdir():
        os.rmdir(target_folder_name)
    status = os.system(f'python3 oura_cdm/main.py {target_folder_name}')
    yield status

    os.rmdir(target_folder_name)
    assert target_folder_name not in os.listdir()


def test_cli_creates_folder(etl_process, target_folder_name):
    assert target_folder_name in os.listdir()


def test_cli_exit_status(etl_process):
    assert etl_process == 0

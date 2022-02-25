import os

import pytest

from oura_cdm.pipeline import run, validate_run, clean_up_run


@pytest.fixture
def pipeline_inputs():
    return {
        "target_folder_name": "sleep_data_test"
    }


@pytest.yield_fixture
def artifacts(pipeline_inputs):
    return run(**pipeline_inputs)


def test_run_valid(artifacts):
    validate_run(artifacts)

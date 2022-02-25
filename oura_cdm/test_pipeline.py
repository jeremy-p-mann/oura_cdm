import os

import pytest

from oura_cdm.pipeline import clean_up_run, run, validate_run


@pytest.fixture
def pipeline_inputs():
    return {
        "target_folder_name": "sleep_data_test"
    }


@pytest.fixture
def artifacts(pipeline_inputs):
    return run(**pipeline_inputs)


@pytest.fixture
def observation_df(artifacts):
    return artifacts['observation_df']


def test_run_valid(artifacts):
    validate_run(artifacts)


def test_observation_concept_ids(observation_df):
    ids = set(observation_df.observation_concept_id.unique())
    allowable_ids = {1001480, 1001932, 1001771}
    assert ids.issubset(allowable_ids)

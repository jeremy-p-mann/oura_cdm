import pytest

from oura_cdm.pipeline import validate_run
from oura_cdm.artifacts import Artifact


@pytest.fixture(scope='session')
def observation_df(pipeline_artifacts):
    return pipeline_artifacts[Artifact.OBSERVATION]


def test_run_valid(pipeline_artifacts):
    validate_run(pipeline_artifacts)


def test_observation_concept_ids(observation_df):
    ids = set(observation_df.observation_concept_id.unique())
    allowable_ids = {1001480, 1001932, 1001771, 1002368}
    assert ids.issubset(allowable_ids)

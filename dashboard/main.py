import streamlit as st

from oura_cdm.pipeline import run
from oura_cdm.pipeline import Artifact


@st.cache
def get_artifacts():
    return run('test_data')


if __name__ == '__main__':
    artifacts = get_artifacts()
    observation_df = artifacts[Artifact.OBSERVATION.value]
    st.dataframe(observation_df)

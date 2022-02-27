import streamlit as st

from oura_cdm.pipeline import run


@st.cache
def get_artifacts():
    return run('test_data')


if __name__ == '__main__':
    artifacts = get_artifacts()
    observation_df = artifacts['observation_df']
    st.dataframe(observation_df)

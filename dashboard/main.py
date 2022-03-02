import altair as alt
import pandas as pd
import streamlit as st
import numpy as np

from oura_cdm.artifacts import Artifact
from oura_cdm.concepts import Ontology
from oura_cdm.pipeline import run


@st.cache
def get_artifacts():
    return run('test_data')


def make_dashboard():
    artifacts = get_artifacts()
    ontology = Ontology()
    observation_df = artifacts[Artifact.OBSERVATION]
    journey_df: pd.DataFrame = artifacts[Artifact.JOURNEY].copy()
    renaming = {c: ontology.get_concept_name_from_id(
        c) for c in journey_df.columns}
    journey_df = journey_df.rename(columns=renaming)
    melted_journey_df = pd.melt(
        journey_df, value_vars=list(journey_df.columns), ignore_index=False)
    duration_column = 'Duration (hours)'
    melted_journey_df[duration_column] = melted_journey_df.value \
        / pd.Timedelta('1 hour')
    melted_journey_df['Duration (hours)'] = np.round(
        melted_journey_df['Duration (hours)'], 2)
    melted_journey_df = melted_journey_df.drop(columns=['value', ])
    melted_journey_df = melted_journey_df.reset_index()
    melted_journey_df['description'] = (
        melted_journey_df['Duration (hours)'].astype(str)
        + 'hours on date '
        + melted_journey_df['observation_date'].astype(str)
        + ' of type '
        + melted_journey_df['observation_concept_id'].astype(str)
    )

    st.write(observation_df)

    single_nearest = alt.selection_single(on='mouseover', nearest=True)
    chart = alt.Chart(melted_journey_df).mark_point().encode(
        x='observation_date',
        y=duration_column,
        color='observation_concept_id',
        tooltip='description'
    ).add_selection(single_nearest).properties(
        width=len(melted_journey_df),
        height=500
    ).interactive()

    st.altair_chart(chart)


if __name__ == '__main__':
    make_dashboard()

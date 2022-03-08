import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

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
    source_data: pd.DataFrame = artifacts[Artifact.SOURCE_DATA]

    renaming = {c: ontology.get_concept_name_from_id(
        c) for c in journey_df.columns}
    journey_df = journey_df.rename(columns=renaming)
    melted_journey_df = pd.melt(
        journey_df, value_vars=list(journey_df.columns), ignore_index=False)
    duration_column = 'Duration (hours)'

    melted_journey_df['minutes'] = (
        (melted_journey_df['value']
         / pd.Timedelta('1 minute')).astype(int)
        % 60
    ).astype(str)
    melted_journey_df['hours'] = (
        (melted_journey_df['value']
         / pd.Timedelta('1 hour')).astype(int)
    ).astype(str)

    melted_journey_df[duration_column] = melted_journey_df.value \
        / pd.Timedelta('1 hour')
    melted_journey_df['Duration (hours)'] = np.round(
        melted_journey_df['Duration (hours)'], 2)
    melted_journey_df = melted_journey_df.drop(columns=['value', ])
    melted_journey_df = melted_journey_df.reset_index()
    melted_journey_df['description'] = (
        + melted_journey_df['hours'] + ':'
        + melted_journey_df['minutes']
        + ' '
        + melted_journey_df['observation_date'].astype(str)
        + ' '
        + melted_journey_df['observation_concept_id'].astype(str)
    )

    st.title("Observation Graph")

    width = min(len(melted_journey_df) * 10, 500)
    single_nearest = alt.selection_single(on='mouseover', nearest=True)
    chart = alt.Chart(melted_journey_df).mark_point().encode(
        x='observation_date',
        y=duration_column,
        color='observation_concept_id',
        tooltip='description'
    ).add_selection(single_nearest).interactive().properties(
        width=width,
    )

    st.altair_chart(chart)

    st.title("Observation Table")
    st.table(observation_df.head(5))
    st.title("Source Data")
    st.write(source_data[0])
    st.title("Ontology Tables")
    st.title("Concepts")
    st.table(artifacts[Artifact.CONCEPT].reset_index())
    st.title("Concept Relationships")
    st.table(artifacts[Artifact.CONCEPT_RELATIONSHIP].reset_index())

if __name__ == '__main__':
    make_dashboard()

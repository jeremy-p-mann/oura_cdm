import altair as alt
import pandas as pd
import streamlit as st

from oura_cdm.artifacts import Artifact
from oura_cdm.concepts import Ontology
from oura_cdm.pipeline import run


@st.cache
def get_artifacts():
    return run()


def make_dashboard():
    artifacts = get_artifacts()
    ontology = Ontology()
    observation_df = artifacts[Artifact.OBSERVATION]
    source_data: pd.DataFrame = artifacts[Artifact.SOURCE_DATA]

    renaming = {c: ontology.get_concept_name_from_id(
        c) for c in observation_df.observation_concept_id.unique()}
    visualization_df = observation_df.copy()
    unit = ontology.get_concept_name(
        ontology.get_concept_from_id(
            observation_df['unit_concept_id'].iloc[0]
        )
    )
    visualization_df["observation_concept_name"] = \
        observation_df.observation_concept_id.replace(renaming)
    renaming = {c: ontology.get_concept_name_from_id(
        c) for c in observation_df.observation_concept_id.unique()}
    visualization_df = visualization_df[
        ['observation_date', 'value_as_number', 'observation_concept_name']]
    visualization_df['observation_date'] = pd.to_datetime(
        visualization_df['observation_date'])
    pd_unit = unit[0].upper()
    time_value = pd.to_timedelta(
        visualization_df['value_as_number'], unit=pd_unit)
    visualization_df['value'] = time_value / pd.Timedelta('1 hour')
    visualization_df['minutes'] = (
        (time_value
         / pd.Timedelta('1 minute')).astype(int)
        % 60
    ).astype(str)
    visualization_df['hours'] = (
        (time_value
         / pd.Timedelta('1 hour')).astype(int)
    ).astype(str)
    visualization_df['description'] = (
        + visualization_df['hours'] + ':'
        + visualization_df['minutes']
        + ' '
        + visualization_df['observation_date'].astype(str)
        + ' '
        + visualization_df['observation_concept_name'].astype(str)
    )

    width = min(len(visualization_df) * 10, 800)
    single_nearest = alt.selection_single(on='mouseover', nearest=True)
    chart = alt.Chart(visualization_df).mark_point().encode(
        x='observation_date',
        y='value',
        color='observation_concept_name',
        tooltip='description'
    ).add_selection(single_nearest).interactive().properties(
        width=width,
    )
    st.altair_chart(chart)
    st.title("Source Data")
    st.write(source_data[0])
    st.title("Observation Table")
    st.table(observation_df.head(5))
    st.title("Ontology Tables")
    st.title("Concepts")
    st.table(artifacts[Artifact.CONCEPT].reset_index())
    st.title("Concept Relationships")
    st.table(artifacts[Artifact.CONCEPT_RELATIONSHIP].reset_index())


if __name__ == '__main__':
    make_dashboard()

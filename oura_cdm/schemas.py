from enum import Enum

import pandera as pa
from pandera.typing import DateTime, Series
from pandera import Column

from oura_cdm.concepts import ObservationConcept


class SleepObservationSchema(pa.SchemaModel):
    observation_id: Series[int] = pa.Field(unique=True)
    person_id: Series[int]
    observation_concept_id: Series[int]
    observation_date: Series[str]
    observation_datetime: Series[DateTime] = pa.Field(nullable=True)
    observation_type_concept_id: Series[int]
    value_as_number: Series[float] = pa.Field(nullable=True)
    value_as_string: Series[str] = pa.Field(nullable=True)
    value_as_concept_id: Series[int] = pa.Field(nullable=True)
    qualifier_concept_id: Series[int] = pa.Field(nullable=True)
    unit_concept_id: Series[int] = pa.Field(nullable=True)
    provider_id: Series[int] = pa.Field(nullable=True)
    visit_occurrence_id: Series[int] = pa.Field(nullable=True)
    visit_detail_id: Series[int] = pa.Field(nullable=True)
    observation_source_value: Series[str] = pa.Field(nullable=True)
    observation_source_concept_id: Series[int] = pa.Field(nullable=True)
    unit_source_value: Series[str] = pa.Field(nullable=True)
    qualifier_source_value: Series[str] = pa.Field(nullable=True)
    value_source_value: Series[str] = pa.Field(nullable=True)
    observation_event_id: Series[int] = pa.Field(nullable=True)
    obs_event_field_concept_id: Series[int] = pa.Field(nullable=True)


def make_journey_schema(observation_df):
    observations = observation_df['observation_concept_id'].unique()
    columns = {
        observation: Column(ObservationConcept.get_dtype(observation))
        for observation in observations
    }
    schema = pa.DataFrameSchema(
        columns
    )
    return schema

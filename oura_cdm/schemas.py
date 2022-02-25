import pandera as pa
from pandera.typing import Series, DateTime


class SleepObservationSchema(pa.SchemaModel):
    observation_id: Series[int]
    person_id: Series[int]
    observation_concept_id: Series[int]
    observation_date: Series[str]
    observation_datetime: Series[DateTime] = pa.Field(nullable=True)
    observation_type_concept_id: Series[int]
    value_as_number: Series[int] = pa.Field(nullable=True)
    value_as_string: Series[int] = pa.Field(nullable=True)
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
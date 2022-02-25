import pandas as pd


def get_observation_table() -> pd.DataFrame:
    return pd.DataFrame({
        "observation_id": [123124],
        "person_id": [1234151],
        "observation_concept_id": [1234142],
        "observation_date": ['20220206'],
        "observation_datetime": [pd.Timestamp('2017-01-01T12')],
        "observation_type_concept_id": [1234152],
        "value_as_number": [None],
        "value_as_string": [None],
        "value_as_concept_id": [None],
        "qualifier_concept_id": [None],
        "unit_concept_id": [None],
        "provider_id": [None],
        "visit_occurrence_id": [None],
        "visit_detail_id": [None],
        "observation_source_value": [None],
        "observation_source_concept_id": [None],
        "unit_source_value": [None],
        "qualifier_source_value": [None],
        "value_source_value": [None],
        "observation_event_id": [None],
        "obs_event_field_concept_id": [None]
    }).astype({
        "value_as_number": 'Int64',
        "value_as_string": 'Int64',
        "value_as_concept_id": 'Int64',
        "qualifier_concept_id": 'Int64',
        "unit_concept_id": 'Int64',
        "provider_id": 'Int64',
        "visit_occurrence_id": 'Int64',
        "visit_detail_id": 'Int64',
        "observation_source_value": 'str',
        "observation_source_concept_id": 'Int64',
        "unit_source_value": 'str',
        "qualifier_source_value": 'str',
        "value_source_value": 'str',
        "observation_event_id": 'Int64',
        "obs_event_field_concept_id": 'Int64'
    }
    )

from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from oura_cdm.concepts import SleepConcept, OuraKeywords


def get_mock_row() -> pd.DataFrame:
    row = pd.DataFrame({
        "observation_id": [123124],
        "person_id": [1234151],
        "observation_concept_id": [SleepConcept.REM_SLEEP_DURATION.value],
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
        "value_as_number": 'float',
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
    })
    return row


def get_observation_table(raw_oura_data: List[Dict]) -> pd.DataFrame:
    transformer = ObservationTransformer(raw_oura_data)
    return transformer.get_transformed_data()


@dataclass
class ObservationTransformer():
    raw_oura_data: List[Dict]

    def get_transformed_data(self,) -> pd.DataFrame:
        mock_row = get_mock_row()
        rows = []
        for i, day in enumerate(self.raw_oura_data):
            for j, concept in enumerate(SleepConcept):
                new_row = mock_row.copy()
                new_row.loc[:, 'observation_id'] = self.get_observation_id(
                    concept, i)
                new_row.loc[:, 'observation_date'] = self.get_observation_date(
                    i)
                new_row.loc[:, 'observation_concept_id'] = concept.value
                rows.append(new_row)
        ans = pd.concat(rows)
        return ans

    def get_observation_date(self, index: int) -> str:
        return self.raw_oura_data[index][OuraKeywords.DATE]

    def get_observation_id(
        self, sleep_concept: SleepConcept, index: int
    ) -> int:
        return sleep_concept.value * (1 + index)

    def get_observation_value(self, concept: SleepConcept) -> float:
        return self.raw_oura_data[
            OuraKeywords.get_keyword_from_concept(concept)
        ]


from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from oura_cdm.concepts import (
    OuraKeywords,
    ObservationConcept,
    ObservationTypeConcept
)


def get_mock_row() -> pd.DataFrame:
    row = pd.DataFrame({
        "observation_id": [123124],
        "person_id": [1234151],
        "observation_concept_id": [ObservationConcept.REM_SLEEP_DURATION.value],
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
            for j, concept in enumerate(ObservationConcept):
                new_row = mock_row.copy()
                new_row.loc[:, 'observation_id'] = self.get_observation_id(
                    concept, i)
                new_row.loc[:, 'observation_date'] = self.get_observation_date(
                    i)
                new_row.loc[:, 'observation_concept_id'] = concept.value
                new_row.loc[:, 'value_as_number'] = self.get_observation_value(
                    i, concept)
                new_row.loc[:, 'value_source_value'] = self.get_value_source_value(
                    i, concept)
                new_row.loc[:, 'observation_type_concept_id'] = self.get_observation_type_id(
                    i, concept)
                new_row.loc[:, 'unit_concept_id'] = self.get_unit_concept_id(
                    i, concept)
                rows.append(new_row)
        ans = pd.concat(rows)
        return ans

    def get_observation_date(self, index: int) -> str:
        return self.raw_oura_data[index][OuraKeywords.DATE]

    def get_observation_id(
        self, sleep_concept: ObservationConcept, index: int
    ) -> int:
        return sleep_concept.value * (1 + index)

    def get_observation_value(self, index: int, concept: ObservationConcept) -> float:
        return float(self.get_value_source_value(index, concept))

    def get_value_source_value(self, index: int, concept: ObservationConcept) -> str:
        return str(self.raw_oura_data[index][
            OuraKeywords.get_keyword_from_concept(concept)
        ])

    def get_observation_type_id(self, index: int, concept: ObservationConcept) -> int:
        return ObservationTypeConcept.LAB.value

    def get_unit_concept_id(self, index: int, concept: ObservationConcept) -> int:
        return ObservationConcept.get_unit_source_id(concept).value

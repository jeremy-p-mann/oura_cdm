from __future__ import annotations

from dataclasses import dataclass
import pkg_resources
from functools import cached_property
from enum import Enum, IntEnum
from typing import List, Type

import pandas as pd


class Concept(IntEnum):
    @classmethod
    def get_all_concepts(cls) -> List[Concept]:
        concepts = []
        concepts += ObservationTypeConcept.get_concepts()
        concepts += UnitConcept.get_concepts()
        concepts += ObservationConcept.get_concepts()
        concepts += OuraConcept.get_concepts()
        return concepts

    @classmethod
    def get_concepts(cls) -> List[Concept]:
        return [c for c in cls]


    @property
    def concept_name(self) -> str:
        return Ontology().get_concept_name(self)


@dataclass
class Ontology():
    @cached_property
    def _concept_df(self,) -> pd.DataFrame:
        stream = pkg_resources.resource_stream(__name__, 'data/concept.csv')
        df = pd.read_csv(stream, sep='\t', index_col='concept_id')
        return df

    def get_concept_name(self, concept: Concept) -> str:
        assert self.is_valid(concept), 'concept not supported'
        return self._concept_df.loc[concept.value, 'concept_name']

    def get_domain_id(self, concept: Concept) -> str:
        assert self.is_valid(concept), 'concept not supported'
        return self._concept_df.loc[concept.value, 'domain_id']

    def is_valid(self, concept: Concept) -> bool:
        return concept.value in self._concept_df.index

    def get_concept_from_id(self, concept_id: int) -> Concept:
        all_concepts = Concept.get_all_concepts()
        concept = [c for c in all_concepts if c.value == concept_id]
        return concept[0]

    def get_concept_name_from_id(self, concept_id) -> str:
        concept = self.get_concept_from_id(concept_id)
        return self.get_concept_name(concept)


class ObservationConcept(Concept, IntEnum):
    REM_SLEEP_DURATION = 1001480
    LIGHT_SLEEP_DURATION = 1001771
    DEEP_SLEEP_DURATION = 1001932
    TOTAL_SLEEP_DURATION = 1002368

    @classmethod
    def get_observation_type_concept_id(
            cls, concept: ObservationConcept) -> int:
        return ObservationTypeConcept.LAB

    @classmethod
    def get_unit_source_id(
            cls, concept: ObservationConcept) -> UnitConcept:
        # RENAME this as it returns a concept
        return UnitConcept.SECOND

    @classmethod
    def get_reference_value(
            cls, concept: ObservationConcept) -> Type:
        return UnitConcept.get_reference_value(cls.get_unit_source_id(concept))

    @classmethod
    def get_domain_id(cls,) -> str:
        return 'Observation'


class ObservationTypeConcept(Concept, IntEnum):
    LAB = 32856

    @classmethod
    def get_domain_id(cls,) -> str:
        return 'Type Concept'


class UnitConcept(Concept, IntEnum):
    SECOND = 8555

    @classmethod
    def get_domain_id(cls,) -> str:
        return 'Unit'

    @classmethod
    def get_reference_value(cls, concept: UnitConcept):
        return pd.Timedelta(1, 's')


class OuraConcept(Concept, IntEnum):
    """
    Strings referenced in Oura's API
    """
    SUMMARY_DATE = 8197349813
    REM = 8197349814
    DEEP = 8197349815
    LIGHT = 8197349816
    TOTAL = 8197349817

    @classmethod
    def get_keyword_from_concept(cls, concept: ObservationConcept):
        return {
            ObservationConcept.REM_SLEEP_DURATION: OuraConcept.REM,
            ObservationConcept.DEEP_SLEEP_DURATION: OuraConcept.DEEP,
            ObservationConcept.LIGHT_SLEEP_DURATION: OuraConcept.LIGHT,
            ObservationConcept.TOTAL_SLEEP_DURATION: OuraConcept.TOTAL,
        }[concept].concept_name

from __future__ import annotations

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
        return concepts

    @classmethod
    def get_concepts(cls) -> List[Concept]:
        return [c for c in cls]


class ObservationConcept(Concept, IntEnum):
    # TODO rename to concept to
    REM_SLEEP_DURATION = 1001480
    LIGHT_SLEEP_DURATION = 1001932
    DEEP_SLEEP_DURATION = 1001771

    @classmethod
    def get_observation_type_concept_id(
            cls, sleep_concept: ObservationConcept) -> int:
        return ObservationTypeConcept.LAB

    @classmethod
    def get_unit_source_id(
            cls, concept: ObservationConcept) -> UnitConcept:
        # RENAME this as it returns a concept
        return UnitConcept.SECOND

    @classmethod
    def get_dtype(
            cls, concept: ObservationConcept) -> Type:
        return UnitConcept.get_dtype(cls.get_unit_source_id(concept))

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
    def get_dtype(cls, concept: UnitConcept) -> Type:
        return pd.Timedelta


class OuraKeywords(str, Enum):
    """
    Strings referenced in Oura's API
    """
    DATE = "summary_date"
    REM = 'rem'
    DEEP = 'deep'
    LIGHT = 'light'

    @classmethod
    def get_keyword_from_concept(cls, concept: ObservationConcept):
        return {
            ObservationConcept.REM_SLEEP_DURATION: OuraKeywords.REM,
            ObservationConcept.DEEP_SLEEP_DURATION: OuraKeywords.DEEP,
            ObservationConcept.LIGHT_SLEEP_DURATION: OuraKeywords.LIGHT,
        }[concept]

from __future__ import annotations

from enum import Enum, IntEnum


class ObservationConcept(IntEnum):
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
        return UnitConcept.SECOND

    @classmethod
    def get_domain_id(cls,) -> str:
        return 'Observation'


class ObservationTypeConcept(IntEnum):
    LAB = 32856

    @classmethod
    def get_domain_id(cls,) -> str:
        return 'Type Concept'


class UnitConcept(IntEnum):
    SECOND = 8555

    @classmethod
    def get_domain_id(cls,) -> str:
        return 'Unit'


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

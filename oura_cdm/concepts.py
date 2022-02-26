from __future__ import annotations

from enum import IntEnum, Enum


class SleepConcept(IntEnum):
    # TODO rename to concept to 
    REM_SLEEP_DURATION = 1001480
    LIGHT_SLEEP_DURATION = 1001932
    DEEP_SLEEP_DURATION = 1001771

    @classmethod
    def get_observation_type_concept_id(
            cls, sleep_concept: SleepConcept) -> int:
        return 32880


class OuraKeywords(str, Enum):
    """
    Strings referenced in Oura's API
    """
    DATE = "summary_date"
    REM = 'rem'
    DEEP = 'deep'
    LIGHT = 'light'

    @classmethod
    def get_keyword_from_concept(cls, concept: SleepConcept):
        return {
            SleepConcept.REM_SLEEP_DURATION: OuraKeywords.REM,
            SleepConcept.DEEP_SLEEP_DURATION: OuraKeywords.DEEP,
            SleepConcept.LIGHT_SLEEP_DURATION: OuraKeywords.LIGHT,
        }[concept]

from __future__ import annotations

from enum import Enum


class SleepConcept(Enum):
    REM_SLEEP_DURATION = 1001480
    LIGHT_SLEEP_DURATION = 1001932
    DEEP_SLEEP_DURATION = 1001771

    @classmethod
    def get_observation_type_concept_id(
            cls, sleep_concept: SleepConcept) -> int:
        return 32880

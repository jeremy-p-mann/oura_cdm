from __future__ import annotations
from enum import Enum


class Artifact(str, Enum):
    JOURNEY = 'journey'
    SOURCE_DATA = 'source'
    OBSERVATION = 'observation'

    @classmethod
    def get_filename(cls, artifact: Artifact):
        return {
            Artifact.JOURNEY: f'{Artifact.JOURNEY}.csv',
            Artifact.SOURCE_DATA: f'{Artifact.SOURCE_DATA}.json',
            Artifact.OBSERVATION: f'{Artifact.OBSERVATION}.csv'
        }[artifact]

    @classmethod
    def validate_function(cls, artifact: Artifact):
        # TODO use this as a for loop in the artifacts
        return {
            Artifact.JOURNEY: f'{Artifact.JOURNEY}.csv',
            Artifact.SOURCE_DATA: f'{Artifact.SOURCE_DATA}.json',
            Artifact.OBSERVATION: f'{Artifact.OBSERVATION}.csv'
        }[artifact]

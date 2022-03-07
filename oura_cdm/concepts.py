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
        concepts += PhysicalConcept.get_concepts()
        return concepts

    @classmethod
    def get_concepts(cls) -> List[Concept]:
        return [c for c in cls]


    @property
    def concept_name(self) -> str:
        return Ontology().get_concept_name(self)

    @property
    def is_standard(self) -> bool:
        return Ontology().get_standard_concept(self) == 'S'



@dataclass
class Ontology():
    @cached_property
    def _concept_df(self,) -> pd.DataFrame:
        stream = pkg_resources.resource_stream(__name__, 'data/concept.csv')
        df = pd.read_csv(stream, sep='\t', index_col='concept_id')
        return df

    @cached_property
    def _concept_relationship_df(self,) -> pd.DataFrame:
        stream = pkg_resources.resource_stream(__name__, 'data/concept_relationship.csv')
        df = pd.read_csv(stream, sep='\t', index_col='concept_id_1')
        return df

    def get_concept_name(self, concept: Concept) -> str:
        assert self.is_valid(concept), 'concept not supported'
        return self._concept_df.loc[concept.value, 'concept_name']

    def get_standard_concept(self, concept: Concept) -> str:
        assert self.is_valid(concept), 'concept not supported'
        return self._concept_df.loc[concept.value, 'standard_concept']

    def get_domain_id(self, concept: Concept) -> str:
        assert self.is_valid(concept), 'concept not supported'
        return self._concept_df.loc[concept.value, 'domain_id']

    def is_valid(self, concept: Concept) -> bool:
        return concept.value in self._concept_df.index

    def get_concept_from_id(self, concept_id: int) -> Concept:
        all_concepts = Concept.get_all_concepts()
        concepts = [c for c in all_concepts if c.value == concept_id]
        assert len(concepts) == 1, f'no concept for id: {concept_id}'
        return concepts[0]

    def get_concept_name_from_id(self, concept_id) -> str:
        concept = self.get_concept_from_id(concept_id)
        return self.get_concept_name(concept)

    def maps_to(self, concept: Concept) -> Concept:
        maps_to_df = self._concept_relationship_df.loc[[concept.value], :]
        ans_ids = maps_to_df[maps_to_df.relationship_id == 'Maps to'].concept_id_2
        assert len(ans_ids) == 1
        ans_id = ans_ids.iloc[0]
        return self.get_concept_from_id(ans_id)


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


class PhysicalConcept(Concept, IntEnum):
    # TODO make sure all of these have units
    DATE = 4260905
    # TIME = 4256606


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
    def get_keyword_from_concept(cls, standard_concept: Concept):
        assert standard_concept.is_standard
        ontology = Ontology()
        translation = {}
        for concept in cls:
            translated_concept = ontology.maps_to(concept)
            translation[translated_concept] = concept
        return translation[standard_concept].concept_name

    # TODO make sure all of these have units


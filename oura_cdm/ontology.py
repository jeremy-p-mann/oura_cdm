from dataclasses import dataclass
import pkg_resources
from functools import cached_property

import pandas as pd

from oura_cdm.concepts import Concept


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

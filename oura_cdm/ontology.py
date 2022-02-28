from dataclasses import dataclass
import pkg_resources
from functools import cached_property

import pandas as pd


@dataclass
class Ontology():
    @cached_property
    def _concept_df(self,) -> pd.DataFrame:
        stream = pkg_resources.resource_stream(__name__, 'data/concept.csv')
        df = pd.read_csv(stream, sep='\t', index_col='concept_id')
        return df

    def get_concept_name(self, concept_id: int) -> str:
        return self._concept_df.loc[concept_id, 'concept_name']

    def get_domain_id(self, concept_id: int) -> str:
        return self._concept_df.loc[concept_id, 'domain_id']

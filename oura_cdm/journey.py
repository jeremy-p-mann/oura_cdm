import pandas as pd

from oura_cdm.concepts import ObservationConcept


def make_observation_journey_df(observation_df: pd.DataFrame) -> pd.DataFrame:
    data = observation_df[
        ['observation_date', 'observation_concept_id', 'value_as_number']
    ]
    ans = pd.pivot_table(
        data=data,
        index='observation_date',
        columns='observation_concept_id',
        values='value_as_number'
    )
    ans.index = pd.DatetimeIndex(ans.index)
    concept_ids = ans.columns
    for c in ans.columns:
        ans[c] = ans[c] * ObservationConcept.get_reference_value(c)
    return ans

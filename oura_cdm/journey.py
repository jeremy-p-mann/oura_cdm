import pandas as pd


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
    return ans

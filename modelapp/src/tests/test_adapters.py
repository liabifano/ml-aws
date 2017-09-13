import pandas as pd
from pandas.util.testing import assert_frame_equal

from modelapp.adapters import json_to_df, SCHEMA_INPUTS


def test_json_to_df():
    request = {'id': '1', 'request_time': '2017-07-27 14:09:16.595260',
               'inputs': {'sepal_length': 1, 'sepal_width': 2, 'pental_length': 3, 'pental_width': 4}}
    expected_result = (pd.DataFrame.from_dict({'id': ['1'],
                                               'sepal_length': [1],
                                               'sepal_width': [2],
                                               'pental_length': [3],
                                               'pental_width': [4],
                                               'request_time': [pd.to_datetime('2017-07-27 14:09:16.595260')]})
                       .astype(SCHEMA_INPUTS))
    result = json_to_df(request)
    assert_frame_equal(expected_result, result, check_like=True)

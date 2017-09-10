import pandas as pd
from pandas.util.testing import assert_frame_equal

from modelapp.adapters import json_to_df


def test_json_to_df():
    request = {'client_id': '1', 'request_time': '2017-07-27 14:09:16.595260', 'inputs': {'a': 3, 'b': 4}}
    expected_result = pd.DataFrame.from_dict({'client_id': ['1'],
                                              'a': [3],
                                              'b': [4],
                                              'request_time': [pd.to_datetime('2017-07-27 14:09:16.595260')]})
    result = json_to_df(request)
    assert_frame_equal(expected_result, result, check_like=True)

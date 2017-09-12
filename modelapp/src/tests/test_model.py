import pandas as pd

from modelapp.model import predict


def test_predict():
    df = pd.DataFrame.from_dict({'a': [1], 'b': [2]})
    result = predict(df)
    expected_result = '1'
    assert expected_result == result

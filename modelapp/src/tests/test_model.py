import pandas as pd
from sklearn.externals import joblib
from modelapp.predict import predictor
from modelapp import config


def test_predictor():
    df = pd.DataFrame.from_dict({'septal_length': [1], 'septal_width': [2], 'pental_length': [3], 'pental_width': [4]})
    trained_model = joblib.load(config.MODEL_PATH)
    result = predictor(df, trained_model)
    expected_result = 'setosa'
    assert expected_result == result

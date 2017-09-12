import pandas as pd

SCHEMA_INPUTS = {'request_time': 'datetime',
                 'id': 'str',
                 'sepal_length': 'float',
                 'sepal_width': 'float',
                 'pental_length': 'float',
                 'pental_width': 'float'}


def coerce_cols_types(col, type):
    #TODO
    return

def json_to_df(request_json):
    df = pd.io.json.json_normalize(request_json)
    df.columns = df.columns.map(lambda x: x.split('.')[-1])
    df['request_time'] = pd.to_datetime(df['request_time']) # xunxo: use coerce_cols_type instead
    return df

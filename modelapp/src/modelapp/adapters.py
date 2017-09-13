import pandas as pd

SCHEMA_INPUTS = {'request_time': 'datetime64[ns]',
                 'id': 'int',
                 'sepal_length': 'float',
                 'sepal_width': 'float',
                 'pental_length': 'float',
                 'pental_width': 'float'}


def json_to_df(request_json):
    df = pd.io.json.json_normalize(request_json)
    df.columns = df.columns.map(lambda x: x.split('.')[-1])
    return df.astype(SCHEMA_INPUTS)

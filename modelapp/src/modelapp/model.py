def predict(df):
    return int((df['a'] + df['b']).iloc[0])
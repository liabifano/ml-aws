LOOKUP_CATEGORY = {0: 'setosa',
                   1: 'versicolor',
                   2: 'virginica'}

def predictor(X, trained_model):
    return LOOKUP_CATEGORY.get(trained_model.predict(X)[0])

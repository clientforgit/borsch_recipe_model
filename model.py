import pandas as pd
from numpy import ravel
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.svm import SVR
import numpy as np


class BasicModel:
    models = {'DecisionTreeRegressor': DecisionTreeRegressor,
              'RandomForestRegressor': RandomForestRegressor,
              'LinearRegression': LinearRegression,
              'Ridge': Ridge,
              'Lasso': Lasso,
              'SVR': SVR}

    def __init__(self, ingredients, prices, model_class_name, *args, **kwargs):
        self.model = self.models[model_class_name](*args, **kwargs, random_state=1)
        self.model.fit(ingredients, ravel(prices))

    def predict(self, val_ingredients: pd.DataFrame):
        return self.model.predict(val_ingredients)

    def mae(self, val_price: pd.DataFrame, val_ingredients: pd.DataFrame):
        return abs(np.array(val_price) - self.predict(val_ingredients)).mean()



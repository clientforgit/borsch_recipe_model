from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.svm import SVR
import numpy as np

from point_dto import PointDTO
from recipes import Recipes
from config_load import config_data


class BasicModel:
    models = {'DecisionTreeRegressor': DecisionTreeRegressor,
              'RandomForestRegressor': RandomForestRegressor,
              'LinearRegression': LinearRegression,
              'Ridge': Ridge,
              'Lasso': Lasso,
              'SVR': SVR}

    def __init__(self, model_class_name, max_deviation=config_data["max_deviation"]):
        self.recipes = Recipes()
        self.model = self.models[model_class_name](random_state=1)
        print(self.recipes.train_ingredients)
        self.model.fit(self.recipes.train_ingredients, self.recipes.train_prices)
        self.predicted_prices = self.model.predict(self.recipes.val_ingredients)
        self.points_list = self.__create_points_list(max_deviation)

    def mae(self):
        return abs(np.array(self.recipes.val_prices) - self.predicted_prices).mean()

    def __create_points_list(self, max_deviation):
        points_list = []
        for i in range(config_data["dataset_size"]):
            if abs(self.recipes.val_prices[i] - self.predicted_prices[i]) < max_deviation:
                color = 'c'
                label = 'in max deviation interval'
            else:
                color = 'r'
                label = 'out of max deviation interval'
            point = PointDTO(
                self.recipes.val_ingredients.loc[i, "calories"],
                self.recipes.val_prices.loc[i],
                color,
                label
            )
            points_list.append(point)

        return points_list



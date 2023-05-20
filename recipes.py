import pandas as pd
import numpy as np
from config_load import config_data
from dataclasses import dataclass


@dataclass
class Dataset:
    ingredients: pd.DataFrame
    prices: pd.Series


class Recipes:
    def __init__(self):
        result = self.generate_dataset()
        self.train_ingredients = result.ingredients
        self.train_prices = result.prices
        result = self.generate_dataset()
        self.val_ingredients = result.ingredients
        self.val_prices = result.prices

    def generate_dataset(self) -> Dataset:
        ingredients = self.__generate_df()
        ingredients_prices = self.__import_properties(['prices'], sep=';', header=0, index_col=0)
        prices = self.__calculate_recipe_property(ingredients, ingredients_prices)
        ingredients_calories = self.__import_properties(['calories'],
                                                        sep=';', header=0, index_col=0).transpose()['calories'].tolist()
        ingredients['calories'] = self.__calculate_recipe_property(ingredients, ingredients_calories)

        return Dataset(ingredients, prices)

    def regenerate(self):
        self.__init__()

    @staticmethod
    def __generate_df() -> pd.DataFrame:
        df = pd.DataFrame(columns=['water', 'beef', 'potato', 'beet', 'carrot',
                                   'onion', 'cabbage', 'tomato_sauce', 'sunflower_oil',
                                   'citric_acid', 'salt', 'sugar', 'bay_leaf'])
        size = config_data['dataset_size']
        df['water'] = [np.random.randint(10, 50) / 10 for i in range(size)]
        df['beef'] = [np.random.randint(0, 25) / 10 for i in range(size)]
        df['potato'] = [np.random.randint(0, 30) / 10 for i in range(size)]
        df['beet'] = [np.random.randint(0, 50) / 100 for i in range(size)]
        df['carrot'] = [np.random.randint(0, 30) / 100 for i in range(size)]
        df['onion'] = [np.random.randint(0, 80) / 100 for i in range(size)]
        df['cabbage'] = [np.random.randint(0, 70) / 100 for i in range(size)]
        df['tomato_sauce'] = [np.random.randint(0, 100) / 1000 for i in range(size)]
        df['sunflower_oil'] = [np.random.randint(0, 50) / 1000 for i in range(size)]
        df['citric_acid'] = [np.random.randint(0, 50) / 1000 for i in range(size)]
        df['salt'] = [np.random.randint(0, 50) / 1000 for i in range(size)]
        df['sugar'] = [np.random.randint(0, 50) / 1000 for i in range(size)]
        df['bay_leaf'] = [np.random.randint(0, 50) / 1000 for i in range(size)]
        return df

    @staticmethod
    def __calculate_recipe_property(ingredients, property) -> pd.Series:
        ingredients_property = np.array(ingredients) * np.array(property)
        recipes_property = pd.Series(ingredients_property.sum(axis=1))
        return recipes_property

    @staticmethod
    def __import_properties(column_names, *args, **kwargs) -> pd.DataFrame:
        properties = pd.read_csv('ingredients_properties.csv', *args, **kwargs)
        property = properties[column_names]
        property = property.transpose()
        return property


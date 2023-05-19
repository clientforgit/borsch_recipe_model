import pandas as pd
import numpy as np
from config_load import config_data


class Recipes:
    def __init__(self):
        self.train_ingredients = self.__generate_df()
        ingredients_prices = self.__import_properties(['ingredients', 'prices'], sep=';', header=0, index_col=0)
        self.train_prices = self.__calculate_price(self.train_ingredients, ingredients_prices)
        self.train_ingredients['calories'] = self.__import_properties(['calories'],
                                                                      sep=';', header=0, index_col=0).transpose()

        self.val_ingredients = self.__generate_df()
        self.val_prices = self.__calculate_price(self.val_ingredients, ingredients_prices)

    def regenerate(self):
        self.__init__()

    @staticmethod
    def __generate_df() -> pd.DataFrame:
        df = pd.DataFrame(columns=['water', 'beef', 'potato', 'beet', 'carrot',
                                   'onion', 'cabbage', 'tomato_sauce', 'sunflower_oil',
                                   'citric_acid', 'salt', 'sugar', 'bay_leaf'])
        size = config_data['dataset_size']
        df['water'] = [np.random.randint(10, 50) / 10 for i in size]
        df['meat'] = [np.random.randint(0, 25) / 10 for i in size]
        df['potato'] = [np.random.randint(0, 30) / 10 for i in size]
        df['beet'] = [np.random.randint(0, 50) / 100 for i in size]
        df['carrot'] = [np.random.randint(0, 30) / 100 for i in size]
        df['onion'] = [np.random.randint(0, 80) / 100 for i in size]
        df['cabbage'] = [np.random.randint(0, 70) / 100 for i in size]
        df['tomato_sauce'] = [np.random.randint(0, 100) / 1000 for i in size]
        df['sunflower_oil'] = [np.random.randint(0, 50) / 1000 for i in size]
        df['citric_acid'] = [np.random.randint(0, 50) / 1000 for i in size]
        df['salt'] = [np.random.randint(0, 50) / 1000 for i in size]
        df['sugar'] = [np.random.randint(0, 50) / 1000 for i in size]
        df['bay_leaf'] = [np.random.randint(0, 50) / 1000 for i in size]

        return df

    @staticmethod
    def __calculate_price(ingredients, prices) -> pd.DataFrame:
        ingredients_prices = np.array(ingredients) * np.array(prices)
        recipes_prices = pd.DataFrame(ingredients_prices.sum(axis=1), columns=['price'])
        # print(recipes_prices.head)
        return recipes_prices

    @staticmethod
    def __import_properties(column_names, *args, **kwargs) -> pd.DataFrame:
        properties = pd.read_csv('ingredients_properties.csv', *args, **kwargs)
        property = properties.loc[:, properties.columns in column_names]
        property = property.transpose()
        # print(prices.head())
        return property


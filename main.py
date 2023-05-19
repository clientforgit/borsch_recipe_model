from model import BasicModel
from recipes import Recipes


def test_max_leaf_nodes(max_leaf_list):
    for max_leaf_nodes in max_leaf_list:
        recipes.regenerate()
        model = BasicModel(recipes.train_ingredients, recipes.train_prices, max_leaf_nodes=max_leaf_nodes)
        print(model.mae(recipes.val_prices, recipes.val_ingredients))


if __name__ == '__main__':
    recipes = Recipes()
    model = BasicModel(recipes.train_ingredients, recipes.train_prices)
    recipes.regenerate()
    predicted_prices = model.predict(recipes.val_ingredients)
    # print(predicted_prices)
    # print(type(predicted_prices))
    print(model.mae(recipes.val_prices, recipes.val_ingredients))
    test_max_leaf_nodes([5, 25, 50, 250, 500, 1000, 2500, 5000])

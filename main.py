

import json
import os
from classes.writer import Writer
from classes.base import RecipeBook


if __name__ == "__main__":
    project_name = "RecipeBooks"
    print("Hello, welcome to the Freebie Content Generator!")
    writer = Writer(project_name)
    writer.write_recipe_using_AI("Generate one healthy very sour breakfast recipe that is good for quick fat loss. Include at least 2 ingredients, but no more than 5 ingredients. Provide cooking time. Provide cooking tips. Provide nutritional information. Give as much detail in each recipe as possible. Do not use fractions of numbers.")
    recipe_book = RecipeBook(project_name)
    recipes = recipe_book.open_json(RecipeBook.RECIPES_FILE_PATH)
    if not isinstance(recipes, list):
        raise ValueError("The JSON content is not a list of recipes.")
    for recipe in recipes:
        recipe_dict = json.loads(recipe)
        print(recipe_dict.get("name"))



# https://pollinations.ai/
# https://image.pollinations.ai/prompt/Lemon-Berry-Blitz-Breakfast
# https://www.desktophut.com/page/free-ai-image-generator

import json
import os
from classes.writer import Writer
from classes.base import RecipeBook


if __name__ == "__main__":
    project_name = "RecipeBooks"
    print("Hello, welcome to the Freebie Content Generator!")
    writer = Writer(project_name)
    system_prompt = "" # TODO update this prompt to make sure it actually does not use recipes in the file
    #try to restructure the generation a bit: first, we generate titles using messages chained together, then we generate the recipes
    # writer.write_recipe_titles_using_AI("Generate a list of 20 healthy breakfast recipe titles of food that is good for quick fat loss. Each should be unique, don't repeat yourself.")
    recipe_book = RecipeBook(project_name)
    recipe_names = recipe_book.open_json(RecipeBook.RECIPE_NAMES_FILE_PATH)
    recipe_names = json.loads(recipe_names[0])
    # Extract the recipe names and print each one 
    for recipe in recipe_names['recipes']:
        # TODO: fix writing to file: it will be one folder for each recipe in a project folder
        writer.write_recipe_using_AI(f"Generate one healthy recipe for {recipe} that is good for quick fat loss. Include at least 2 ingredients, but no more than 5 ingredients. Provide cooking time. Provide cooking tips. Provide nutritional information. Give as much detail in each recipe as possible. Do not use fractions of numbers.", system_prompt)




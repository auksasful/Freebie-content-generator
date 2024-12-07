# https://pollinations.ai/
# https://image.pollinations.ai/prompt/Lemon-Berry-Blitz-Breakfast
# https://www.desktophut.com/page/free-ai-image-generator

import json
import os
from classes.writer import Writer
from classes.base import RecipeBook


def generate_recipe_titles(writer, system_prompt):
    writer.write_recipe_titles_using_AI("Generate a list of 20 healthy breakfast recipe titles of food that is good for quick fat loss. Each should be unique, don't repeat yourself.")

def generate_recipes(writer, system_prompt):
    recipe_book = RecipeBook(project_name, book_name)
    recipe_names = recipe_book.open_json(RecipeBook.RECIPE_NAMES_FILE_PATH)
    recipe_names = json.loads(recipe_names[0])
    for recipe in recipe_names['recipes']:
        writer.write_recipe_using_AI(f"Generate one healthy recipe for {recipe['name']} that is good for quick fat loss. Include at least 2 ingredients, but no more than 5 ingredients. Provide cooking time. Provide cooking tips. Provide nutritional information. Give as much detail in each recipe as possible. Do not use fractions of numbers.", system_prompt, recipe['name'])

if __name__ == "__main__":
    project_name = "RecipeBooks"
    book_name = "Healthy Breakfast Recipes"
    print("Hello, welcome to the Freebie Content Generator!")
    writer = Writer(project_name, book_name)
    system_prompt = ""
    # generate_recipe_titles(writer, system_prompt)
    # generate_recipes(writer, system_prompt)

    recipe_book = RecipeBook(project_name, book_name)
    recipe_names = recipe_book.open_json(RecipeBook.RECIPE_NAMES_FILE_PATH)
    recipe_names = json.loads(recipe_names[0])
    for recipe in recipe_names['recipes']:
        recipe_text = recipe_book.open_json(recipe_book.RECIPES_FILE_PATH, recipe['name'])
        recipe_data = json.loads(recipe_text[0])
        print(f"{recipe_data['name']} : {recipe_data['ingredients']}")




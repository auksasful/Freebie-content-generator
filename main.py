# https://pollinations.ai/
# https://image.pollinations.ai/prompt/Lemon-Berry-Blitz-Breakfast
# https://www.desktophut.com/page/free-ai-image-generator

import json
import os
from classes.base_recipebook_generator import BaseRecipebookGenerator
from classes.writer import Writer
from classes.base import RecipeBook

from PIL import Image, ImageDraw, ImageFont
import requests
import time
from datetime import datetime
import uuid


def generate_recipe_titles(writer, system_prompt):
    writer.write_recipe_titles_using_AI("Generate a list of 20 healthy breakfast recipe titles of food that is good for quick fat loss. Each should be unique, don't repeat yourself.")

def generate_recipes(writer, system_prompt):
    recipe_book = RecipeBook(project_name, book_name)
    recipe_names = recipe_book.open_json(RecipeBook.RECIPE_NAMES_FILE_PATH)
    recipe_names = json.loads(recipe_names[0])
    for recipe in recipe_names['recipes']:
        writer.write_recipe_using_AI(f"Generate one healthy recipe for {recipe['name']} that is good for quick fat loss. Include at least 2 ingredients, but no more than 5 ingredients. Provide cooking time. Provide cooking tips. Provide nutritional information. Make the instructions short but understandable. Do not use fractions of numbers.", system_prompt, recipe['name'])
        time.sleep(10)
        
def generate_recipebook_page_images(project_name, book_name):
    recipe_book = RecipeBook(project_name, book_name)
    recipe_names = recipe_book.open_json(RecipeBook.RECIPE_NAMES_FILE_PATH)
    recipe_names = json.loads(recipe_names[0])
    recipebook_generator1 = BaseRecipebookGenerator(project_name, book_name, RecipeBook.GENERATOR_MODE_1)
    recipebook_generator2 = BaseRecipebookGenerator(project_name, book_name, RecipeBook.GENERATOR_MODE_2)
    for i, recipe in enumerate(recipe_names['recipes']):
        recipe_text = recipe_book.open_json(recipe_book.RECIPES_FILE_PATH, recipe['name'])
        recipe_data = json.loads(recipe_text[0])
        print(f"{recipe_data['name']} : {recipe_data['ingredients']}")
        recipebook_generator2.create_recipe_page(recipe_data, i + 1)
        recipebook_generator1.create_recipe_page(recipe_data, i + 1)

def evaluate_recipebook_pages(project_name, book_name):
    recipebook_generator = BaseRecipebookGenerator(project_name, book_name, RecipeBook.GENERATOR_MODE_1)
    recipebook_generator.evaluate_pages()

def create_cover_page(project_name, book_name):
    cover_generator = BaseRecipebookGenerator(project_name, book_name, RecipeBook.GENERATOR_MODE_1)
    cover_generator.create_cover_page()

def export_recipebook_to_pdf(project_name, book_name):
    recipebook_generator = BaseRecipebookGenerator(project_name, book_name, RecipeBook.GENERATOR_MODE_1)
    recipebook_generator.export_to_pdf()


if __name__ == "__main__":
    project_name = "RecipeBooks"
    book_name = "Healthy Breakfast Recipes"
    print("Hello, welcome to the Freebie Content Generator!")
    writer = Writer(project_name, book_name)
    system_prompt = ""
    # generate_recipe_titles(writer, system_prompt)
    # generate_recipes(writer, system_prompt)
    # generate_recipebook_page_images(project_name, book_name)
    # create_cover_page(project_name, book_name)
    # evaluate_recipebook_pages(project_name, book_name)
    export_recipebook_to_pdf(project_name, book_name) # TODO


    



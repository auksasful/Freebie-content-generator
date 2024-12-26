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
from classes.settings import RecipeBookSettings


def generate_recipe_titles(writer, prompt):
    writer.write_recipe_titles_using_AI(prompt)

def generate_recipes(writer, system_prompt, prompt_1, prompt_2):
    recipe_book = RecipeBook(project_name, book_name)
    recipe_names = recipe_book.open_json(RecipeBook.RECIPE_NAMES_FILE_PATH)
    recipe_names = json.loads(recipe_names[0])
    for recipe in recipe_names['recipes']:
        writer.write_recipe_using_AI(f"{prompt_1} {recipe['name']} {prompt_2}", system_prompt, recipe['name'])
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
    settings = RecipeBookSettings()
    system_prompt = settings.system_prompt

    while True:
        print("\nPlease select an action:")
        print("1. Generate titles")
        print("2. Generate the entries")
        print("3. Generate book page images")
        print("4. Create cover page")
        print("5. Evaluate book pages")
        print("6. Export book to PDF")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            generate_recipe_titles(writer, settings.titles_prompt)
        elif choice == '2':
            generate_recipes(writer, system_prompt, settings.generation_prompt_1, settings.generation_prompt_2)
        elif choice == '3':
            generate_recipebook_page_images(project_name, book_name)
        elif choice == '4':
            create_cover_page(project_name, book_name)
        elif choice == '5':
            evaluate_recipebook_pages(project_name, book_name)
        elif choice == '6':
            export_recipebook_to_pdf(project_name, book_name)
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


    



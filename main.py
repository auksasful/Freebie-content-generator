# https://pollinations.ai/
# https://image.pollinations.ai/prompt/Lemon-Berry-Blitz-Breakfast
# https://www.desktophut.com/page/free-ai-image-generator

import json
import os
from classes.base_recipebook_generator import BaseRecipebookGenerator
from classes.base_tipsbook_generator import BaseTipsbookGenerator
from classes.writer import Writer
from classes.base import Book

from PIL import Image, ImageDraw, ImageFont
import requests
import time
from datetime import datetime
import uuid
from classes.settings import RecipeBookSettings, TipsBookSettings


def generate_titles(writer, prompt, project_name):
    if project_name == "RecipeBooks":
        writer.write_recipe_titles_using_AI(prompt)
    elif project_name == "TipsBooks":
        writer.write_tip_titles_using_AI(prompt)

def generate_data(writer, system_prompt, prompt_1, prompt_2, project_name):
    book = Book(project_name, book_name)
    names = book.open_json(Book.NAMES_FILE_PATH)
    names = json.loads(names[0])
    if project_name == "RecipeBooks":
        iterate_through = names['recipes']
    elif project_name == "TipsBooks":
        iterate_through = names['tips']
    for name in iterate_through:
        if project_name == "RecipeBooks":
            writer.write_recipe_using_AI(f"{prompt_1} {name['name']} {prompt_2}", system_prompt, name['name'])
        elif project_name == "TipsBooks":
            writer.write_tip_using_AI(f"{prompt_1} {name['name']} {prompt_2}", system_prompt, name['name'])
        time.sleep(10)
        
def generate_book_page_images(project_name, book_name):
    book = Book(project_name, book_name)
    names = book.open_json(Book.NAMES_FILE_PATH)
    names = json.loads(names[0])
    if project_name == "RecipeBooks":
        recipebook_generator1 = BaseRecipebookGenerator(project_name, book_name, Book.GENERATOR_MODE_1)
        recipebook_generator2 = BaseRecipebookGenerator(project_name, book_name, Book.GENERATOR_MODE_2)
        for i, recipe in enumerate(names['recipes']):
            recipe_text = book.open_json(book.DATA_LIST_FILE_PATH, recipe['name'])
            recipe_data = json.loads(recipe_text[0])
            print(f"{recipe_data['name']} : {recipe_data['ingredients']}")
            recipebook_generator2.create_recipe_page(recipe_data, i + 1)
            recipebook_generator1.create_recipe_page(recipe_data, i + 1)
    elif project_name == "TipsBooks":
        tipsbook_generator1 = BaseTipsbookGenerator(project_name, book_name, Book.GENERATOR_MODE_1)
        tipsbook_generator2 = BaseTipsbookGenerator(project_name, book_name, Book.GENERATOR_MODE_2)
        for i, tip in enumerate(names['tips']):
            tip_text = book.open_json(book.DATA_LIST_FILE_PATH, tip['name'])
            tip_data = json.loads(tip_text[0])
            if 'name' in tip_data:
                if tip_data['name']:
                    print(f"{tip_data['name']} : {tip_data['description']}")
                    tipsbook_generator2.create_tip_page(tip_data, i + 1)
                    tipsbook_generator1.create_tip_page(tip_data, i + 1)

def evaluate_book_pages(project_name, book_name):
    if project_name == "TipsBooks":
        tipsbook_generator = BaseTipsbookGenerator(project_name, book_name, Book.GENERATOR_MODE_1)
        tipsbook_generator.evaluate_pages()
    elif project_name == "RecipeBooks":
        recipebook_generator = BaseRecipebookGenerator(project_name, book_name, Book.GENERATOR_MODE_1)
        recipebook_generator.evaluate_pages()

def create_cover_page(project_name, book_name):
    if project_name == "TipsBooks":
        cover_generator = BaseTipsbookGenerator(project_name, book_name, Book.GENERATOR_MODE_1)
    elif project_name == "RecipeBooks":
        cover_generator = BaseRecipebookGenerator(project_name, book_name, Book.GENERATOR_MODE_1)
    cover_generator.create_cover_page()

def export_book_to_pdf(project_name, book_name):
    if project_name == "TipsBooks":
        tipsbook_generator = BaseTipsbookGenerator(project_name, book_name, Book.GENERATOR_MODE_1)
        tipsbook_generator.export_to_pdf()
    elif project_name == "RecipeBooks":
        recipebook_generator = BaseRecipebookGenerator(project_name, book_name, Book.GENERATOR_MODE_1)
        recipebook_generator.export_to_pdf()


if __name__ == "__main__":
    print("Hello, welcome to the Freebie Content Generator!")

    ### CHANGE THIS TO YOUR BOOK NAME
    book_name = "Easy Photo Editing Tips"
    project_name = "TipsBooks"
    # project_name = "RecipeBooks"
    ### CHANGE THIS TO YOUR BOOK NAME

    writer = Writer(project_name, book_name)
    if project_name == "RecipeBooks":
        settings = RecipeBookSettings()
    elif project_name == "TipsBooks":
        settings = TipsBookSettings()
    else:
        settings = None
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
            title_prompt = settings.titles_prompt_1 + book_name + settings.titles_prompt_2
            generate_titles(writer, title_prompt, project_name)
        elif choice == '2':
            generate_data(writer, system_prompt, settings.generation_prompt_1, settings.generation_prompt_2, project_name)
        elif choice == '3':
            generate_book_page_images(project_name, book_name)
        elif choice == '4':
            create_cover_page(project_name, book_name)
        elif choice == '5':
            evaluate_book_pages(project_name, book_name)
        elif choice == '6':
            export_book_to_pdf(project_name, book_name)
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


    



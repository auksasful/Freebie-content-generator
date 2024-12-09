# https://pollinations.ai/
# https://image.pollinations.ai/prompt/Lemon-Berry-Blitz-Breakfast
# https://www.desktophut.com/page/free-ai-image-generator

import json
import os
from classes.writer import Writer
from classes.base import RecipeBook

from PIL import Image, ImageDraw, ImageFont


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

    # recipe_book = RecipeBook(project_name, book_name)
    # recipe_names = recipe_book.open_json(RecipeBook.RECIPE_NAMES_FILE_PATH)
    # recipe_names = json.loads(recipe_names[0])
    # for recipe in recipe_names['recipes']:
    #     recipe_text = recipe_book.open_json(recipe_book.RECIPES_FILE_PATH, recipe['name'])
    #     recipe_data = json.loads(recipe_text[0])
    #     print(f"{recipe_data['name']} : {recipe_data['ingredients']}")


    # Load images
    image1 = Image.open("image1.png")
    image2 = Image.open("image2.png")

    # Create a new blank image with white background
    width, height = 800, 1200
    new_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(new_image)

    # Define fonts
    title_font = ImageFont.truetype("arial.ttf", 40)
    subtitle_font = ImageFont.truetype("arial.ttf", 30)
    text_font = ImageFont.truetype("arial.ttf", 20)

    # Add title
    draw.text((3 * width // 4 - 100, 20), "Creamy Pasta", font=title_font, fill="black")

    # Add servings and time
    draw.text((3 * width // 4 - 100, 80), "2 servings", font=text_font, fill="black")
    draw.text((3 * width // 4, 80), "15 minutes", font=text_font, fill="black")

    # Add ingredients title
    draw.text((3 * width // 4 - 100, 120), "INGREDIENTS", font=subtitle_font, fill="black")

    # Add ingredients list
    ingredients = [
        "100 ml milk",
        "50 g butter",
        "3 eggs",
        "1 tbs cocoa",
        "2 tsp baking soda",
        "a pinch of salt",
        "3 eggs"
    ]
    y_position = 160
    for ingredient in ingredients:
        draw.text((3 * width // 4 - 100, y_position), ingredient, font=text_font, fill="black")
        y_position += 30

    # Add directions title
    draw.text((50, height - 600), "DIRECTIONS", font=subtitle_font, fill="black")

    # Add directions text (Lorem ipsum)
    directions = [
        "1. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo.",
        "2. Donec dictum lectus in ex accumsan sodales. Pellentesque habitant morbi tristique.",
        "3. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo. Donec dictum lectus in ex. Lentesque habitant morbi tristique. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo. Donec dictum lectus in ex.",
        "4. Habitant morbi tristique. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo."
    ]
    y_position = height - 550
    max_width = width // 2 - 100  # 50 percent of the page width

    for direction in directions:
        lines = []
        words = direction.split()
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=text_font)[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        for line in lines:
            draw.text((50, y_position), line, font=text_font, fill="black")
            y_position += 30

    # Resize images to take half of the page horizontally and vertically
    image1 = image1.resize((width // 2, height // 2))
    image2 = image2.resize((width // 2, height // 2))

    # Paste images
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (width // 2, height // 2))

    # Save the final image
    new_image.save("recipe_card.png")




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

def template_1_page_generator(image1_path, image2_path, stopwatch_path, title, time, ingredients, directions, save_path):
    # Load images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    stopwatch = Image.open(stopwatch_path)

    # Create a new blank image with white background
    width, height = 800, 1200
    new_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(new_image)

    # Define fonts
    title_font = ImageFont.truetype("brushscript.ttf", 40)
    subtitle_font = ImageFont.truetype("georgia.ttf", 30)
    text_font = ImageFont.truetype("arial.ttf", 20)

    # Add title
    draw.text((3 * width // 4 - 180, 20), title, font=title_font, fill="black")

    # Add time
    stopwatch = stopwatch.resize((30, 30))  # Resize the stopwatch image
    new_image.paste(stopwatch, (3 * width // 4 - 180, 75))  # Paste the stopwatch image
    draw.text((3 * width // 4 - 145, 80), time, font=text_font, fill="black")

    # Add ingredients title
    draw.text((3 * width // 4 - 180, 120), "INGREDIENTS", font=subtitle_font, fill="black")

    # Add ingredients list
    y_position = 160
    for ingredient in ingredients:
        draw.text((3 * width // 4 - 180, y_position), ingredient, font=text_font, fill="black")
        y_position += 30

    # Add directions title
    draw.text((20, height - 590), "DIRECTIONS", font=subtitle_font, fill="black")

    # Add directions text
    y_position = height - 540
    max_width = width // 2 - 20  # 50 percent of the page width

    for direction in directions:
        lines = []
        words = direction.split()
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=text_font)[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        for line in lines:
            draw.text((20, y_position), line, font=text_font, fill="black")
            y_position += 30

    # Resize images to take half of the page horizontally and vertically
    image1 = image1.resize((width // 2, height // 2))
    image2 = image2.resize((width // 2, height // 2))

    # Paste images
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (width // 2, height // 2))

    # Save the final image
    new_image.save(save_path)


def template_2_page_generator(image1_path, image2_path, image3_path, stopwatch_path, title, time, ingredients, directions, save_path):
    # Load images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    image3 = Image.open(image3_path)
    stopwatch = Image.open(stopwatch_path)

    # Create a new blank image with white background
    width, height = 800, 1200
    new_image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(new_image)

    # Define fonts
    title_font = ImageFont.truetype("brushscript.ttf", 40)
    subtitle_font = ImageFont.truetype("georgia.ttf", 30)
    text_font = ImageFont.truetype("arial.ttf", 20)

    # Add title
    draw.text((3 * width // 4 - 180, 20), title, font=title_font, fill="black")

    # Add time
    stopwatch = stopwatch.resize((30, 30))  # Resize the stopwatch image
    new_image.paste(stopwatch, (3 * width // 4 - 180, 75))  # Paste the stopwatch image
    draw.text((3 * width // 4 - 145, 80), time, font=text_font, fill="black")

    # Add ingredients title
    draw.text((3 * width // 4 - 180, 120), "INGREDIENTS", font=subtitle_font, fill="black")

    # Add ingredients list
    y_position = 160
    for ingredient in ingredients:
        draw.text((3 * width // 4 - 180, y_position), ingredient, font=text_font, fill="black")
        y_position += 30

    # Add directions title
    draw.text((20, height - 590), "DIRECTIONS", font=subtitle_font, fill="black")

    # Add directions text
    y_position = height - 540
    max_width = width // 2 - 20  # 50 percent of the page width

    for direction in directions:
        lines = []
        words = direction.split()
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=text_font)[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        for line in lines:
            draw.text((20, y_position), line, font=text_font, fill="black")
            y_position += 30


    # Resize images to take half of the page horizontally and vertically
    # Define margins
    margin = 10

    # Crop 40% from top and bottom
    crop_height = int(image1.height * 0.32)
    crop_width = int(image1.width * 0.1)
    image1 = image1.crop((crop_width, crop_height, image1.width - crop_width, image1.height - crop_height))
    image2 = image2.crop((crop_width, crop_height, image2.width - crop_width, image2.height - crop_height))

    # Resize images to take half of the page horizontally and vertically
    image1 = image1.resize((image1.width // 2 - 2 * margin, image1.height // 2))
    image2 = image2.resize((image2.width // 2 - 2 * margin, image2.height // 2))
    image3 = image3.resize((image3.width // 2 + 200 - 2 * margin, image3.height // 2))

    # Paste images with margins
    new_image.paste(image1, (margin, 0))
    new_image.paste(image2, (width // 2 + margin, 0))
    new_image.paste(image3, (width // 4 + margin, height - image3.height - margin))

    # Save the final image
    new_image.save(save_path)


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



    template_1_page_generator(
        image1_path="image1.png",
        image2_path="image2.png",
        stopwatch_path="stopwatch.png",
        title="Creamy Pasta",
        time="15 minutes",
        ingredients=[
            "100 ml milk",
            "50 g butter",
            "3 eggs",
            "1 tbs cocoa",
            "2 tsp baking soda",
            "a pinch of salt",
            "3 eggs"
        ],
        directions=[
            "1. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo.",
            "2. Donec dictum lectus in ex accumsan sodales. Pellentesque habitant morbi tristique.",
            "3. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo. Donec dictum lectus in ex. Luctus tristique. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo. Donec dictum lectus in ex.",
            "4. Habitant morbi tristique. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo."
        ],
        save_path="template_1_output.png"
    )

    template_2_page_generator(
    image1_path="image1.png",
    image2_path="image2.png",
    image3_path="image3.png",
    stopwatch_path="stopwatch.png",
    title="Creamy Pasta",
    time="15 minutes",
    ingredients=[
        "100 ml milk",
        "50 g butter",
        "3 eggs",
        "1 tbs cocoa",
        "2 tsp baking soda",
        "a pinch of salt",
        "3 eggs"
    ],
    directions=[
        "1. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo.",
        "2. Donec dictum lectus in ex accumsan sodales. Pellentesque habitant morbi tristique.",
        "3. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo. Donec dictum lectus in ex. Luctus tristique. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo. Donec dictum lectus in ex.",
        "4. Habitant morbi tristique. Nunc nulla velit, feugiat vitae ex quis, lobortis porta leo."
    ],
    save_path="template_2_output.png"
    )


    



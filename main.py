# https://pollinations.ai/
# https://image.pollinations.ai/prompt/Lemon-Berry-Blitz-Breakfast
# https://www.desktophut.com/page/free-ai-image-generator

import json
import os
from classes.writer import Writer
from classes.base import RecipeBook

from PIL import Image, ImageDraw, ImageFont
import requests
import time
from datetime import datetime


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
    title_font = ImageFont.truetype("brushscript.ttf", 55)
    subtitle_font = ImageFont.truetype("georgia.ttf", 30)
    text_font = ImageFont.truetype("arial.ttf", 20)

    # Add title
    draw.text((3 * width // 4 - 180, 10), title, font=title_font, fill="black")

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


def template_2_page_generator(image1_path, image2_path, image3_path, stopwatch_path, title, title2, time, ingredients, directions, save_path):
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
    title_font = ImageFont.truetype("brushscript.ttf", 80)
    title2_font = ImageFont.truetype("brushscript.ttf", 50)
    subtitle_font = ImageFont.truetype("georgia.ttf", 30)
    text_font = ImageFont.truetype("arial.ttf", 20)

    # Add title
    draw.text((50, height // 2 - 330), title, font=title_font, fill="black")
    draw.text((50, height // 2 - 235), title2, font=title2_font, fill="black")

    # Add time
    stopwatch = stopwatch.resize((30, 30))  # Resize the stopwatch image
    new_image.paste(stopwatch, (width - 200, height // 2 - 190))  # Paste the stopwatch image
    draw.text((width - 165, height // 2 - 185), time, font=text_font, fill="black")

    # Add ingredients title
    draw.text((75, height // 2 - 120), "INGREDIENTS", font=subtitle_font, fill="black")

    # Add ingredients list
    y_position = height // 2 - 80
    for ingredient in ingredients:
        draw.text((75, y_position), ingredient, font=text_font, fill="black")
        y_position += 30

    # Add directions title
    draw.text((width // 2 - 50, height // 2 - 120), "DIRECTIONS", font=subtitle_font, fill="black")

    # Add directions text
    y_position = height // 2 - 80
    max_width = width // 2 + 20  # 50 percent of the page width

    for direction in directions:
        lines = []
        words = direction.split()
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=text_font)[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        for line in lines:
            draw.text((width // 2 - 50, y_position), line, font=text_font, fill="black")
            y_position += 30


    # Resize images to take half of the page horizontally and vertically
    # Define margins
    margin = 10

    # Crop 40% from top and bottom
    crop_height = int(image1.height * 0.32)
    crop_width = int(image1.width * 0.1)
    image3_crop_height = int(image3.height * 0.4)
    image3_crop_width = int(image3.width * 0.15)
    image1 = image1.crop((crop_width, crop_height, image1.width - crop_width, image1.height - crop_height))
    image2 = image2.crop((crop_width, crop_height, image2.width - crop_width, image2.height - crop_height))
    image3 = image3.crop((image3_crop_width, image3_crop_height, image3.width - image3_crop_width, image3.height - image3_crop_height))
    # Draw a line in the middle of the new image, leaving a bit of space from left and right
    line_margin = 65
    draw.line(
        [(line_margin, height // 2 - 150), (width - line_margin, height // 2 - 150)],
        fill="black",
        width=3
    )

    draw.line(
        [(width // 2 - 100, height // 2 - 115), (width // 2 - 100, height // 2 + 425)],
        fill="black",
        width=3
    )

    # Resize images to take half of the page horizontally and vertically
    image1 = image1.resize((image1.width // 2 - 2 * margin, image1.height // 2))
    image2 = image2.resize((image2.width // 2 - 2 * margin, image2.height // 2))
    image3 = image3.resize((image3.width // 2 + 80, image3.height // 2))

    # Paste images with margins
    new_image.paste(image1, (margin, 0))
    new_image.paste(image2, (width // 2 + margin, 0))
    new_image.paste(image3, (25, height - image3.height))

    # Save the final image
    new_image.save(save_path)



def generate_recipe_images_pollynation_ai(prompt, save_path):
    # Format the prompt for the URL
    formatted_prompt = prompt.replace(" ", "-")
    url = f"https://image.pollinations.ai/prompt/{formatted_prompt}"

    # Make the request to the API
    response = requests.get(url)
    if response.status_code == 200:
        # Wait for the image to be generated
        # time.sleep(10)  # Adjust the sleep time as needed

        # Save the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_save_path = save_path.replace("img_", f"img_{timestamp}_")
        with open(image_save_path, 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to generate image. Status code: {response.status_code}")

    # Open the saved image
    image = Image.open(image_save_path)

    # Crop 50 pixels from the bottom
    image = image.crop((0, 0, image.width, image.height - 48))

    # Calculate the new dimensions for cropping
    width, height = image.size
    crop_height = int((width - 170) * 1.2)

    # Crop the image to the new dimensions
    left = 85
    top = (height - crop_height) / 2
    right = width - 85
    bottom = (height + crop_height) / 2
    cropped_image = image.crop((left, top, right, bottom))

    # Save the cropped image
    cropped_image.save(image_save_path)


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

    generate_recipe_images_pollynation_ai("Creamy Pasta with sausages from farther distance", "image1.png")
    generate_recipe_images_pollynation_ai("Creamy Pasta with kebab in a kiosk", "image2.png")
    generate_recipe_images_pollynation_ai("Creamy Pasta with milk a lot of milk", "image3.png")


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

    # TODO fix the image sizes
    template_2_page_generator(
    image1_path="image1.png",
    image2_path="image2.png",
    image3_path="image3.png",
    stopwatch_path="stopwatch.png",
    title="Creamy Pasta",
    title2="With delicious sauce",
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


    




from datetime import datetime
import os
import re
import time
import uuid

import requests
from classes.base import RecipeBook

from PIL import Image, ImageDraw, ImageFont


class BaseRecipebookGenerator(RecipeBook):

    TEMPLATES = ['template_1', 'template_2']


    def __init__(self, project_folder, book, template, width = 1000, height = 1200):
        super().__init__(project_folder, book)
        self.width = width
        self.height = height
        self.template = template
        self.project_assets_path = os.path.join(self.project_path, 'assets')
        self.project_pages_path = os.path.join(self.project_path, 'pages')
        self.project_images_path = os.path.join(self.project_assets_path, 'images')
        self.stopwatch_path = 'common_assets'
        os.makedirs(self.project_images_path, exist_ok=True)
        os.makedirs(self.project_pages_path, exist_ok=True)
        os.makedirs(self.project_assets_path, exist_ok=True)
        os.makedirs(self.stopwatch_path, exist_ok=True)
        self.stopwatch_path = os.path.join(self.stopwatch_path, 'stopwatch.png')

    def create_cover_page(self):
        pass

    def create_table_of_contents(self):
        pass

    def create_recipe_page(self, recipe):
        if self.template == self.TEMPLATES[0]:
            from classes.template1_recipebook_generator import Template1RecipebookGenerator
            recipe_generator = Template1RecipebookGenerator(self.project_assets_path, self.book, self.template, self.width, self.height)
        elif self.template == self.TEMPLATES[1]:
            from classes.template2_recipebook_generator import Template2RecipebookGenerator
            recipe_generator = Template2RecipebookGenerator()
        else:
            raise ValueError('Invalid template')
        

        title1 = self.remove_symbols(recipe['name']) + str(uuid.uuid4())
        title2 = self.remove_symbols(recipe['name']) + str(uuid.uuid4())
        image1_path = self.generate_recipe_images_pollynation_ai(title1, recipe['name'], self.project_images_path)
        image2_path = self.generate_recipe_images_pollynation_ai(title2, recipe['name'], self.project_images_path)
        project_pages_path_for_image = os.path.join(self.project_pages_path, recipe['name'])
        recipe_generator.generate_page(image1_path, image2_path, self.stopwatch_path, recipe['name'], recipe['cooking_time'], recipe['ingredients'], recipe['instructions'], project_pages_path_for_image)
        
    def generate_recipe_images_pollynation_ai(self, prompt, title_original, save_path):
        # Format the prompt for the URL
        formatted_prompt = prompt.replace(" ", "-")
        url = f"https://image.pollinations.ai/prompt/{formatted_prompt}"

        while True:
            # Make the request to the API
            response = requests.get(url)
            if response.status_code == 200:
                # Wait for the image to be generated
                # time.sleep(10)  # Adjust the sleep time as needed

                # Save the image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_save_path = os.path.join(save_path, title_original, f"img_{timestamp}.png")
                os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
                with open(image_save_path, 'wb') as f:
                    f.write(response.content)
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
                return image_save_path
            else:
                print(f"Failed to generate image. Status code: {response.status_code}. Retrying...")
                time.sleep(5)  # Wait for 5 seconds before retrying

    @staticmethod
    def remove_symbols(text): 
        # Replace non-space symbols with an empty string 
        return re.sub(r'[^\w\s]', '', text)

    def generate_page(self, image1_path, image2_path, stopwatch_path, title, time, ingredients, directions, save_path):
        raise NotImplementedError('generate_image method must be implemented in child class')

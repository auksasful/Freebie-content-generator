
import os
from classes.base import RecipeBook


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
        os.makedirs(self.project_images_path, exist_ok=True)
        os.makedirs(self.project_pages_path, exist_ok=True)
        os.makedirs(self.project_assets_path, exist_ok=True)

    def create_cover_page(self):
        pass

    def create_table_of_contents(self):
        pass

    def create_recipe_page(self, recipe):
        pass

    def generate_page(self, image1_path, image2_path, stopwatch_path, title, time, ingredients, directions, save_path):
        raise NotImplementedError('generate_image method must be implemented in child class')

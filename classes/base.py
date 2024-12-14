import json
import os


class RecipeBook:
    RECIPES_FILE_PATH = 'recipes.txt'
    RECIPE_NAMES_FILE_PATH = 'recipe_names.txt'

    GENERATOR_MODE_1 = 'template_1'
    GENERATOR_MODE_2 = 'template_2'


    def __init__(self, project_folder, book) -> None:
        self.book = book
        self.project_path = os.path.join(os.path.abspath('projects'), project_folder)
        self.project_path = os.path.join(self.project_path, book)
       
    
    def write_json(self, data, filename, page = ''):
        if page != '':
            data_file_path = os.path.join(self.project_path, page, filename)
        else:
            data_file_path = os.path.join(self.project_path, filename)
        file_exists = os.path.isfile(data_file_path)
        if not file_exists:
            os.makedirs(os.path.dirname(data_file_path), exist_ok=True)
            with open(data_file_path, 'w', encoding='utf-8') as file:
                json.dump([], file)
        file_empty = os.path.exists(data_file_path) and os.stat(data_file_path).st_size == 0

        if (filename == self.RECIPES_FILE_PATH or filename == self.RECIPE_NAMES_FILE_PATH) and not file_empty:
            with open(data_file_path, 'r+', encoding='utf-8') as file:
                file_data = json.load(file)
                file_data.append(data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        else:
            with open(data_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
    

    def open_json(self, filename, page = ''):
        if page != '':
            data_file_path = os.path.join(self.project_path, page, filename)
        else:
            data_file_path = os.path.join(self.project_path, filename)
        if os.path.isfile(data_file_path):
            with open(data_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return None
    
    def initialize_page(self, page):
        page_path = os.path.join(self.project_path, page)
        os.makedirs(page_path, exist_ok=True)
        return page_path

    def get_sheets_data(self):
        pass

    def call_gemini(self, system_prompt, message):
        pass

    



import json
import os


class RecipeBook:
    RECIPES_FILE_PATH = 'recipes.json'


    def __init__(self, project_folder) -> None:
        self.project_path = os.path.join(os.path.abspath('projects'), project_folder)
    
    def write_json(self, data, filename):
        data_file_path = os.path.join(self.project_path, filename)
        file_exists = os.path.isfile(data_file_path)
        if not file_exists:
            os.makedirs(os.path.dirname(data_file_path), exist_ok=True)
            with open(data_file_path, 'w', encoding='utf-8') as file:
                json.dump([], file)
        file_empty = os.path.exists(data_file_path) and os.stat(data_file_path).st_size == 0

        if filename == self.RECIPES_FILE_PATH and not file_empty:
            with open(data_file_path, 'r+', encoding='utf-8') as file:
                file_data = json.load(file)
                file_data.append(data)
                file.seek(0)
                json.dump(file_data, file, indent=4)
        else:
            with open(data_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
    

    def open_json(self, filename):
        data_file_path = os.path.join(self.project_path, filename)
        if os.path.isfile(data_file_path):
            with open(data_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return None

    def get_sheets_data(self):
        pass

    def call_gemini(self, system_prompt, message):
        pass

    



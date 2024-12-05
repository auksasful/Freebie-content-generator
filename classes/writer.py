
from classes.base import RecipeBook
from entities.recipe import Recipe
import google.generativeai as genai
import json
import os


class Writer(RecipeBook):
    
    def __init__(self, project_folder) -> None:
        super().__init__(project_folder)
    
    def write_recipe_using_AI(self, prompt, system_prompt):
        api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=system_prompt)
        response = model.generate_content([prompt, self.RECIPES_FILE_PATH])
        raw_data = response.text
        prompt = f"""
        Summarize the recipe based on the schema given.

        {raw_data}"""
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "response_schema": Recipe})
        try:
            # Attempt to parse the response text as JSON
            data = json.loads(response.text)
            # If successful, print the formatted JSON
            # print(json.dumps(data, indent=4))
        except json.JSONDecodeError as e:
            # If parsing fails, print the error and the raw response text
            print(f"Error decoding JSON: {e}")
            print(f"Raw response text: {response.text}")
        self.write_json(response.text, self.RECIPES_FILE_PATH)



    def write_recipe_name(self, recipe):
        pass

    def write_ingredients(self, ingredients):
        pass

    def write_instructions(self, instructions):
        pass

    def write_cooking_tips(self, tips):
        pass

    def write_nutrition_facts(self, nutrition):
        pass


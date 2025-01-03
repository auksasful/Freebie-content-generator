
from classes.base import Book
from entities.recipe import Recipe
from entities.recipe import RecipesNames
from entities.tip import TipNames
from entities.tip import Tip
import google.generativeai as genai
import json
import os
import re


class Writer(Book):
    
    def __init__(self, project_folder, book) -> None:
        super().__init__(project_folder, book)
    
    def write_recipe_titles_using_AI(self, prompt, api_key):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(prompt)
        raw_data = response.text
        prompt = f"""
        Write the recipes based on the schema given.

        {raw_data}"""
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "response_schema": RecipesNames})
        try:
            # Attempt to parse the response text as JSON
            data = json.loads(response.text)
            # If successful, print the formatted JSON
            # print(json.dumps(data, indent=4))
        except json.JSONDecodeError as e:
            # If parsing fails, print the error and the raw response text
            print(f"Error decoding JSON: {e}")
            print(f"Raw response text: {response.text}")
            recipe_names = json.loads(response.text)
            # Extract the recipe names and sanitize each one
            for recipe in recipe_names['recipes']:
                sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', recipe['name'])
                recipe['name'] = sanitized_name
                self.initialize_page(sanitized_name)
            # Write to file after all pages have been initialized
            self.write_json(json.dumps(recipe_names), self.NAMES_FILE_PATH)  # return response.text


    def write_recipe_using_AI(self, prompt, system_prompt, page, api_key):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='gemini-1.5-flash') #, system_instruction=system_prompt)
        response = model.generate_content(prompt)
        # response = model.generate_content([prompt, self.RECIPES_FILE_PATH])
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
        self.write_json(response.text, self.DATA_LIST_FILE_PATH, page)



    def write_tip_titles_using_AI(self, prompt, api_key):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        response = model.generate_content(prompt)
        raw_data = response.text
        prompt = f"""
        Write the tips based on the schema given.

        {raw_data}"""
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "response_schema": TipNames})
        try:
            # Attempt to parse the response text as JSON
            data = json.loads(response.text)
            # If successful, print the formatted JSON
            # print(json.dumps(data, indent=4))
        except json.JSONDecodeError as e:
            # If parsing fails, print the error and the raw response text
            print(f"Error decoding JSON: {e}")
            print(f"Raw response text: {response.text}")

        tip_names = json.loads(response.text)
        # Extract the tip names and sanitize each one
        for tip in tip_names['tips']:
            sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', tip['name'])
            tip['name'] = sanitized_name
            self.initialize_page(sanitized_name)
        # Write to file after all pages have been initialized
        self.write_json(json.dumps(tip_names), self.NAMES_FILE_PATH)  # return response.text


    def write_tip_using_AI(self, prompt, system_prompt, page, api_key):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name='gemini-1.5-flash') #, system_instruction=system_prompt)
        response = model.generate_content(prompt)
        # response = model.generate_content([prompt, self.RECIPES_FILE_PATH])
        raw_data = response.text
        prompt = f"""
        Summarize the tip based on the schema given.

        {raw_data}"""
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json", "response_schema": Tip})
        try:
            # Attempt to parse the response text as JSON
            data = json.loads(response.text)
            # If successful, print the formatted JSON
            # print(json.dumps(data, indent=4))
        except json.JSONDecodeError as e:
            # If parsing fails, print the error and the raw response text
            print(f"Error decoding JSON: {e}")
            print(f"Raw response text: {response.text}")
        self.write_json(response.text, self.DATA_LIST_FILE_PATH, page)




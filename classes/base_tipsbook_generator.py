
from datetime import datetime
import os
import re
import time
import uuid

import requests
from classes.base import Book

from PIL import Image, ImageDraw, ImageFont, ImageTk
import shutil
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF

from classes.settings import TipsBookSettings

class BaseTipsbookGenerator(Book):

    TEMPLATES = ['template_1', 'template_2']


    def __init__(self, project_folder, book, template, width = 1000, height = 1200):
        super().__init__(project_folder, book)
        self.width = width
        self.height = height
        self.template = template
        self.project_folder = project_folder
        self.book = book
        self.project_assets_path = os.path.join(self.project_path, 'assets')
        self.project_pages_path = os.path.join(self.project_path, 'pages')
        self.project_images_path = os.path.join(self.project_assets_path, 'images')
        self.stopwatch_path = 'common_assets'
        os.makedirs(self.project_images_path, exist_ok=True)
        os.makedirs(self.project_pages_path, exist_ok=True)
        os.makedirs(self.project_assets_path, exist_ok=True)
        os.makedirs(self.stopwatch_path, exist_ok=True)
        self.stopwatch_path = os.path.join(self.stopwatch_path, 'stopwatch.png')
        self.settings = TipsBookSettings()

    def create_cover_page(self):
        from classes.cover_page_generator import CoverPageGenerator
        cover_generator = CoverPageGenerator(self.project_folder, self.book, self.width, self.height)
        cover_image1_path = self.generate_images_pollynation_ai(self.settings.cover_page_image1_prompt + self.book + str(uuid.uuid4()), self.book, self.project_images_path)
        cover_image2_path = self.generate_images_pollynation_ai(self.settings.cover_page_image2_prompt + self.book + str(uuid.uuid4()), self.book, self.project_images_path)
        cover_generator.generate_cover(cover_image1_path, cover_image2_path, self.book, self.project_pages_path)

    def create_table_of_contents(self):
        pass

    def create_tip_page(self, tip, page_number=1):
        if self.template == self.TEMPLATES[0]:
            from classes.template1_tipsbook_generator import Template1TipsbookGenerator
            tips_generator = Template1TipsbookGenerator(self.project_assets_path, self.book, self.template, self.width, self.height)
        elif self.template == self.TEMPLATES[1]:
            from classes.template2_tipsbook_generator import Template2TipsbookGenerator
            tips_generator = Template2TipsbookGenerator(self.project_assets_path, self.book, self.template, self.width, self.height)
        else:
            raise ValueError('Invalid template')
        
        image_prompt_default = self.settings.image_prompt_default
        dish_placeholder = self.remove_symbols(tip['name'])
        image_prompt_bottom = f'{self.settings.image_prompt_bottom_1} {dish_placeholder} {self.settings.image_prompt_bottom_2}'

        if self.template == self.TEMPLATES[0]:
            title1 = self.remove_symbols(tip['name']) + str(uuid.uuid4())
            title2 = self.remove_symbols(tip['name']) + str(uuid.uuid4())
            image1_path = self.generate_images_pollynation_ai(image_prompt_default + title1, tip['name'], self.project_images_path)
            image2_path = self.generate_images_pollynation_ai(image_prompt_default + title2, tip['name'], self.project_images_path)
            tips_generator.generate_page(image1_path, image2_path, tip['name'], tip['description'], tip['instructions'], self.project_pages_path, page_number)
        elif self.template == self.TEMPLATES[1]:
            name_parts = tip['name'].split()
            if len(name_parts) <= 3:
                title1 = name_parts[0]
                title2 = name_parts[-1]
            elif len(name_parts) >= 7:
                title1 = ' '.join(name_parts[:-5])
                title2 = ' '.join(name_parts[-5:])
            else:
                title1 = ' '.join(name_parts[:-3])
                title2 = ' '.join(name_parts[-3:])
            image1_path = self.generate_images_pollynation_ai(image_prompt_default + self.remove_symbols(tip['name']) + str(uuid.uuid4()), tip['name'], self.project_images_path)
            image2_path = self.generate_images_pollynation_ai(image_prompt_default + self.remove_symbols(tip['name']) + str(uuid.uuid4()), tip['name'], self.project_images_path)
            image3_path = self.generate_images_pollynation_ai(image_prompt_bottom + str(uuid.uuid4()), tip['name'], self.project_images_path)
            tips_generator.generate_page(image1_path, image2_path, image3_path, title1, title2,  tip['description'], tip['instructions'], self.project_pages_path, page_number)


    def generate_images_pollynation_ai(self, prompt, title_original, save_path):
        # Format the prompt for the URL
        formatted_prompt = prompt.replace(" ", "-")
        url = f"https://image.pollinations.ai/prompt/{formatted_prompt}"

        while True:
            try:
                # Make the request to the API
                response = requests.get(url)
                if response.status_code == 200:
                    # Wait for the image to be generated
                    # time.sleep(10)  # Adjust the sleep time as needed

                    # Save the image
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    sanitized_title = self.remove_symbols(title_original)
                    image_save_path = os.path.join(save_path, sanitized_title, f"img_{timestamp}.png")
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
            except requests.RequestException as e:
                print(f"Request failed: {e}. Retrying...")
            time.sleep(5)  # Wait for 5 seconds before retrying

    def evaluate_pages(self):
        self.image_evaluator_app(self.project_pages_path)

    def export_to_pdf(self):

        def add_url_to_page(pdf, url, y_pos):
            pdf.set_y(y_pos)
            pdf.set_font("Arial", size=12)
            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 10, url, 0, 1, 'C', link=url)

        def add_page_number(pdf, page_num, page_number_y):
            pdf.set_y(page_number_y)
            pdf.set_font("Arial", size=8)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, f'{page_num}', 0, 0, 'R')

        # Initialize PDF
        pdf = FPDF()
        liked_images_folder = os.path.join(self.project_pages_path, 'liked_images')

        if not os.path.exists(liked_images_folder):
            messagebox.showinfo("Info", "No liked images found to export.")
            return

        image_files = [f for f in os.listdir(liked_images_folder)
                    if f.lower().endswith(('png', 'jpg', 'jpeg'))]

        if not image_files:
            messagebox.showinfo("Info", "No liked images found to export.")
            return

        # Handle cover image
        cover_image = None
        for image_file in image_files:
            if image_file.startswith('cover;'):
                cover_image = image_file
                break

        if cover_image:
            image_files.remove(cover_image)
            image_files.insert(0, cover_image)

        # Set margins
        left_margin = right_margin = 10
        top_margin = 10
        bottom_margin = 10
        pdf.set_margins(left_margin, top_margin, right_margin)

        pdf_w = pdf.w - left_margin - right_margin
        pdf_h = pdf.h - top_margin - bottom_margin

        # Approximate height for URL text and space after image
        space_after_image = 5  # Space after image

        # Process images
        for idx, image_file in enumerate(image_files):
            image_path = os.path.join(liked_images_folder, image_file)
            pdf.add_page()

            # Determine whether to display URL
            if idx == 0 and cover_image:
                display_url = False
                url_h = 0  # No URL on cover page
            else:
                display_url = True
                url_h = 10  # Height of URL text

            # Add URL if needed
            if display_url:
                url_y = top_margin
                add_url_to_page(pdf, self.settings.website_url, y_pos=url_y)

            # Open image to get dimensions
            with Image.open(image_path) as img:
                img_w_px, img_h_px = img.size

            img_ratio = img_w_px / img_h_px

            # Calculate max dimensions
            max_w = pdf_w
            max_h = pdf_h - url_h - space_after_image

            # Calculate image dimensions to fit within max dimensions
            if (max_w / img_ratio) <= max_h:
                display_w = max_w
                display_h = display_w / img_ratio
            else:
                display_h = max_h
                display_w = display_h * img_ratio

            # Center the image
            x = (pdf.w - display_w) / 2
            y = top_margin + url_h + ((max_h - display_h) / 2)

            pdf.image(image_path, x=x, y=y, w=display_w, h=display_h)

            # Add page number if not the first page
            if idx != 0:
                page_number_y = top_margin
                add_page_number(pdf, idx + 1, page_number_y)

        output_pdf_path = os.path.join(self.project_path, 'tip_book.pdf')
        pdf.output(output_pdf_path)
        messagebox.showinfo("Info", f"PDF exported successfully to {output_pdf_path}")

    @staticmethod
    def remove_symbols(text): 
        # Replace non-space symbols with an empty string 
        return re.sub(r'[^\w\s]', '', text)
    
    @staticmethod
    def image_evaluator_app(save_image_path):
        source_folder = save_image_path
        liked_target_folder = os.path.join(source_folder, 'liked_images')

        # Get list of images in the source folder
        image_files = [f for f in os.listdir(source_folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
        
        if not image_files:
            messagebox.showinfo("Info", "No images found in the specified folder.")
            return

        if not os.path.exists(liked_target_folder):
            os.makedirs(liked_target_folder)

        def group_images_by_set(image_files):
            image_sets = {}
            for image_file in image_files:
                set_number = image_file.split(';')[0]
                if set_number not in image_sets:
                    image_sets[set_number] = []
                image_sets[set_number].append(image_file)
            return list(image_sets.values())

        image_sets = group_images_by_set(image_files)

        root = tk.Tk()
        root.title("Image Evaluator")
        root.geometry("1800x1200")  # Set the window size to be 3 times bigger

        canvas = tk.Canvas(root)
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def show_images(image_set):
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            row = 0
            col = 0
            for image_file in image_set:
                image_path = os.path.join(source_folder, image_file)
                image = Image.open(image_path)
                if len(image_set) > 3:
                    image.thumbnail((300, 300))
                else:
                    image.thumbnail((600, 600))
                photo = ImageTk.PhotoImage(image)
                image_label = tk.Label(scrollable_frame, image=photo)
                image_label.image = photo
                image_label.grid(row=row, column=col)
                image_label.bind("<Button-1>", lambda e, img_file=image_file: image_clicked(img_file))
                col += 1
                if col > 2:
                    col = 0
                    row += 1

        def image_clicked(image_file):
            image_path = os.path.join(source_folder, image_file)
            shutil.move(image_path, os.path.join(liked_target_folder, image_file))
            next_set()

        def next_set():
            if image_sets:
                current_set = image_sets.pop(0)
                show_images(current_set)
            else:
                messagebox.showinfo("Info", "All images have been evaluated.")
                root.destroy()

        next_set()
        root.mainloop()

        def image_clicked(image_file):
            image_path = os.path.join(source_folder, image_file)
            shutil.move(image_path, os.path.join(liked_target_folder, image_file))
            next_set()

        def next_set():
            if image_sets:
                current_set = image_sets.pop(0)
                show_images(current_set)
            else:
                messagebox.showinfo("Info", "All images have been evaluated.")
                root.destroy()

        next_set()
        root.mainloop()

    def generate_page(self, image1_path, image2_path, stopwatch_path, title, time, ingredients, directions, save_path):
        raise NotImplementedError('generate_image method must be implemented in child class')

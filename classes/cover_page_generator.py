import os
import uuid
from PIL import Image, ImageDraw, ImageFont
from classes.base import Book

class CoverPageGenerator(Book):

    def __init__(self, project_folder, book, width=1000, height=1200):
        super().__init__(project_folder, book)

    def generate_cover(self, image1_path, image2_path, title, save_path):
        cover_image, draw = self.create_blank_image(800, 1200)
        title_font, subtitle_font, author_font = self.define_fonts()

        self.add_cover_image(cover_image, image1_path, 800)
        self.add_cover_image(cover_image, image2_path, 900, position_x=0, position_y=700)
        self.add_cover_title(draw, title, title_font, 800, 620)
        self.add_warm_filter(cover_image)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        save_path = os.path.join(save_path, 'cover;' + str(uuid.uuid4()) + '.png')

        cover_image.save(save_path)


    def create_blank_image(self, width, height):
        new_image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(new_image)
        return new_image, draw
        
    def add_cover_image(self, cover_image, image_path, max_width, max_height=None, position_x=0, position_y=0):
        image = Image.open(image_path)
        aspect_ratio = image.width / image.height
        if max_height is None:
            max_height = int(max_width / aspect_ratio)
        elif max_width / max_height > aspect_ratio:
            max_width = int(max_height * aspect_ratio)
        else:
            max_height = int(max_width / aspect_ratio)
        image = image.resize((max_width, max_height))
        
        # Crop 20% from the top and 20% from the bottom
        crop_height = int(image.height * 0.2)
        image = image.crop((0, crop_height, image.width, image.height - crop_height))
        
        cover_image.paste(image, (position_x, position_y))

    def add_cover_title(self, draw, title, title_font, width, y_position):
        max_width = width - 20
        words = title.split()
        lines = []
        while words:
            line = ''
            while words and draw.textbbox((0, 0), line + words[0], font=title_font)[2] <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        for line in lines:
            draw.text((width // 2 - draw.textbbox((0, 0), line, font=title_font)[2] // 2, y_position), line, font=title_font, fill="black")
            y_position += 60

    def add_warm_filter(self, image):
        width, height = image.size
        pixels = image.load()
        for py in range(height):
            for px in range(width):
                r, g, b = image.getpixel((px, py))

                tr = int(r * 1.2)
                tg = int(g * 1.1)
                tb = int(b * 0.9)

                if tr > 255:
                    tr = 255

                if tg > 255:
                    tg = 255

                if tb > 255:
                    tb = 255

                pixels[px, py] = (tr, tg, tb)

    def define_fonts(self):
        title_font = ImageFont.truetype("brushscript.ttf", 60)
        subtitle_font = ImageFont.truetype("georgia.ttf", 40)
        author_font = ImageFont.truetype("arial.ttf", 30)
        return title_font, subtitle_font, author_font

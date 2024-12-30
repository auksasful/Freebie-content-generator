# Freebie content generator

Freebie content generator is bot for generating informative PDFs

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the packages from requirements.txt.

```bash
pip install -r requirements.txt
```

## Usage
In the main method, assign these values as preferred:
```python
if __name__ == "__main__":
    print("Hello, welcome to the Freebie Content Generator!")

    ### CHANGE THIS TO YOUR BOOK NAME
    book_name = "Cyber Security Tips"
    project_name = "TipsBooks"
    # project_name = "RecipeBooks"
    api_key = os.getenv('GOOGLE_API_KEY') # Define your Gemini API key as an environment variable (recommended) or just replace this with your API key (not recommended)
    ### CHANGE THIS TO YOUR BOOK NAME
```
book_name - it is the name of your book, it will reflect the topic.

project_name - it is the type of project you are making, currently there can be RecipeBooks or TipsBooks.

api_key - it is the API key that you can get for free from [Google AI Studio](https://aistudio.google.com/apikey).

After that, you can modify the prompts based on your project in settings.py, located in classes folder.

When running the bot, you will see a menu like this:
```bash
Hello, welcome to the Freebie Content Generator!

Please select an action:    
1. Generate titles
2. Generate the entries     
3. Generate book page images
4. Create cover page        
5. Evaluate book pages      
6. Export book to PDF       
7. Exit
Enter your choice: 
```
Then you should enter numbers one after another, starting from 1 (titles generation), ending with 6 (export to PDF).

This takes a while to finish, especially the book page images.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
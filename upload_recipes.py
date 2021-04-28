import os
from dotenv import load_dotenv
from websites.seriouseats import get_recipes
from schedule_function.db import RecipeDB


if __name__ == "__main__":
    load_dotenv()
    DB_URL = os.environ['DB_HOST_URL']
    db = RecipeDB(DB_URL)

    recipes = get_recipes("https://www.seriouseats.com/recipes/topics/meal/soups?page=", "#recipes", 1, 25)

    db.insert_recipes(recipes, "dessert")

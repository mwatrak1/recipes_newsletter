from cloud_function.db import RecipeDB
import unittest
from dotenv import load_dotenv
import os


class TestDB(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        db_url = os.environ['DB_HOST_URL']
        self.db = RecipeDB(db_url)

    def tearDown(self):
        self.db.close_connection()

    def test_get_meals(self):
        meals = self.db.meals
        self.assertIsInstance(meals, list)
        for meal in meals:
            self.assertIsInstance(meal, str)

    def test_generate_meal_recipe(self):
        recipe = self.db.generate_meal_recipe('main course')
        print(recipe)
        self.assertIsInstance(recipe, dict)
        self.assertTrue("title" in recipe.keys())
        self.assertTrue("recipe_link" in recipe.keys())
        self.assertIsInstance(recipe.get("ingredients", None), list)

    def test_generate_random_recipes(self):
        recipes = self.db.generate_random_recipes()
        self.assertIsInstance(recipes, dict)

        for meal, recipe in recipes.items():
            self.assertIsInstance(meal, str)
            self.assertIsInstance(recipe, dict)
            # self.assertTrue("ingredients" in recipe.keys(), "no ingredients attribute")
            # self.assertTrue("directions" in recipe.keys(), "no directions attribute")


if __name__ == '__main__':
    unittest.main()

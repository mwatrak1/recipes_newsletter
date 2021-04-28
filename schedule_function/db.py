from pymongo import MongoClient


# make it into context manager
class RecipeDB:
    def __init__(self, db_url):
        self.client = MongoClient(db_url)
        self.db = self.client.get_database("recipes_newsletter")
        self.user_db = self.client.get_database("recipes_users")
        self.meals = self.get_meals()

    def insert_recipes(self, recipes, collection_name):
        for recipe in recipes:
            self.db[collection_name].insert_one(recipe)

    def close_connection(self):
        self.client.close()

    def generate_random_recipes(self):
        random_recipes = {}
        for meal in self.meals:
            recipe = self.generate_meal_recipe(meal)
            if recipe:
                random_recipes[meal] = recipe
        return random_recipes

    def generate_meal_recipe(self, meal):
        try:
            random_recipe_cursor = self.db[meal].aggregate([{"$sample": {"size": 1}}])
            random_recipe = next(random_recipe_cursor)
        except StopIteration:
            print("No documents found exception!")
            return False
        return random_recipe

    def get_meals(self):
        return list(self.db.list_collection_names())

    def get_users_emails(self):
        users = self.user_db.get_collection("users").find({})
        emails = []

        for user in users:
            users_email = user.get("email")
            if users_email:
                emails.append(users_email)

        return emails

    def select_meal_recipes(self, meal):
        pass

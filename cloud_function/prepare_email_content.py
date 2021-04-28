from dotenv import load_dotenv
from db import RecipeDB
import os

load_dotenv()
db_url = os.environ['DB_HOST_URL']
client = RecipeDB(db_url)


def generate_random_recipes():
    return client.generate_random_recipes()


def get_users_emails():
    return client.get_users_emails()

from bs4 import BeautifulSoup
from requests import request
import time
import concurrent.futures


recipes = []


def get_recipes_metadata(url_start, url_end, start_page=1, end_page=1):

    recipes_titles_and_links = []

    for index in range(start_page, end_page + 1):
        recipe_list = request("GET", url_start + str(index) + url_end)
        soup = BeautifulSoup(recipe_list.text, "lxml")
        recipe_cards_section = soup.find("section", attrs={"class": "c-cards--3-wide"})
        recipe_cards = recipe_cards_section.find_all("article")

        for recipe in recipe_cards:
            recipe_link = recipe.a["href"]
            recipe_item_text = recipe.find("div", attrs={"class": "c-card__text-container"})
            recipe_title_div = recipe_item_text.h4.a
            recipe_title = recipe_title_div.string

            if recipe_title is None:
                continue

            recipes_titles_and_links.append({
                "recipe_title": recipe_title,
                "recipe_link": recipe_link
            })
    return recipes_titles_and_links


def validate_field(field_name):
    if field_name is not None and len(field_name) > 0:
        return True


def get_directions(recipe_soup):
    directions_div = recipe_soup.find("div", attrs={"class": "recipe-procedures"})
    directions_paragraphs = directions_div.find_all("div", attrs={"class": "recipe-procedure-text"})

    directions = [direction.string for direction_paragraph in directions_paragraphs
                  for direction in direction_paragraph if direction != "\n" and direction is not None]

    if validate_field(directions) is None:
        return False
    directions = list(filter(lambda x: x is not None, directions))
    return directions


def get_ingredients(ingredients_div):
    ingredients_li_elements = ingredients_div.find_all("li", attrs={"class": "ingredient"})
    ingredients = [ingredient.string for ingredient in ingredients_li_elements]

    if validate_field(ingredients) is None:
        return False
    return ingredients


def get_recipe_photo(recipe_soup):
    recipe_photo = recipe_soup.find("img", attrs={"class": "photo"})
    if recipe_photo is None:
        recipe_photo = "https://automatycznyjadlospis.s3.eu-central-1.amazonaws.com/food.jpg"
    else:
        recipe_photo = recipe_photo.get("src")
    return recipe_photo


def get_recipe_info(recipe_soup):
    recipe_info = recipe_soup.find_all("span", attrs={"class": "info"})[:3]
    return recipe_info


def assemble_recipe(recipe_soup, title, recipe_link):
    recipe_photo = get_recipe_photo(recipe_soup)

    recipe_info = get_recipe_info(recipe_soup)

    try:
        recipe_yield, recipe_active_cooking_time, recipe_total_cooking_time = recipe_info
    except ValueError:
        return False

    try:
        ingredients_div = recipe_soup.find("div", attrs={"class": "recipe-ingredients"}).ul
    except AttributeError:
        return False

    directions = get_directions(recipe_soup)

    ingredients = get_ingredients(ingredients_div)

    title = title.strip("/").strip("\\")

    if ingredients and directions and recipe_total_cooking_time and ingredients_div:
        recipes.append({
            "title": title,
            "ingredients": ingredients,
            "directions": directions,
            "yield": recipe_yield.string,
            "active_time": recipe_active_cooking_time.string,
            "total_time": recipe_total_cooking_time.string,
            "photo_link": recipe_photo,
            "recipe_link": recipe_link
        })
        print(title)


def get_recipes(url_start, url_end, start_page=1, end_page=1):
    recipes_metadata = get_recipes_metadata(url_start, url_end, start_page, end_page)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(request_soup_and_assemble_recipe, recipes_metadata)

    return recipes


def request_soup_and_assemble_recipe(recipe):
    recipe_page = request("GET", recipe["recipe_link"])
    recipe_soup = BeautifulSoup(recipe_page.text, "lxml")
    assemble_recipe(recipe_soup, recipe["recipe_title"], recipe["recipe_link"])


if __name__ == "__main__":
    start_time = time.perf_counter()
    get_recipes("https://www.seriouseats.com/recipes/topics/meal/mains?page=", "#recipes", 1, 1)
    end_time = time.perf_counter()
    print(f'Finished in {end_time-start_time} second(s)')

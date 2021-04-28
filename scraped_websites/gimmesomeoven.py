import concurrent.futures
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from requests import request

recipes = []


def get_recipes_metadata(url_start, url_end, start_page=1, end_page=1):

    recipes_titles_and_links = []

    for index in range(start_page, end_page + 1):
        recipe_list = request("GET", url_start + str(index) + url_end)
        soup = BeautifulSoup(recipe_list.text, "lxml")
        recipe_cards_section = soup.find("div", attrs={"class": "teaser-posts"})
        recipe_cards = recipe_cards_section.find_all("div", {"class": "teaser-post-sm"})

        for recipe in recipe_cards:
            recipe_link = recipe.a["href"]
            recipe_title = recipe.a["title"]

            if recipe_title is None:
                print("No title")
                continue

            recipes_titles_and_links.append({
                "recipe_title": recipe_title,
                "recipe_link": recipe_link
            })

    return recipes_titles_and_links


def check_blacklist_words(text):
    blacklist = ["How To", "Your Favorite", "My Favorite", "100+"]

    for word in blacklist:
        if word in text:
            return True
    return False


def get_recipe_photo(recipe_soup):
    recipe_photo = recipe_soup.find("div", attrs={"class": "post"}).find("img")

    if recipe_photo is None:
        recipe_photo = "https://automatycznyjadlospis.s3.eu-central-1.amazonaws.com/food.jpg"
    else:
        recipe_photo = recipe_photo.get("src")

    return recipe_photo


def get_recipe_info(recipe_soup):
    info = {}
    try:
        recipe_yield_spans = recipe_soup.find("span", attrs={"class": "tasty-recipes-yield"}).find_all("span")
        info['recipe_yield'] = recipe_yield_spans[0].string + " to " + recipe_yield_spans[1].string
        info['recipe_active_cooking_time'] = recipe_soup.find("span", attrs={"class": "tasty-recipes-cook-time"}).string
        info['recipe_total_cooking_time'] = recipe_soup.find("span", attrs={"class": "tasty-recipes-total-time"}).string
    except AttributeError:
        return False
    return info


def get_ingredients(ingredients_div):
    ingredients_li_elements = ingredients_div.find_all("li")
    ingredients = []

    for ingredient in ingredients_li_elements:
        ingredients_text = ""

        for element in ingredient:
            if element.name == "span":
                try:
                    ingredients_text += element.string
                except TypeError:
                    continue
            if isinstance(element, NavigableString):
                try:
                    ingredients_text += element.string
                except TypeError:
                    continue
            if element.name == "a":
                try:
                    ingredients_text += element.string
                except TypeError:
                    continue
        ingredients.append(ingredients_text)
    return ingredients


def get_directions(directions_div):
    directions_paragraphs = directions_div.find_all("li")
    directions = []

    for direction in directions_paragraphs:
        directions_text = ""

        for element in direction:
            if element.name == "span":
                try:
                    directions_text += element.string
                except TypeError:
                    continue
            if isinstance(element, NavigableString):
                try:
                    directions_text += element.string
                except TypeError:
                    continue
            if element.name == "a":
                try:
                    directions_text += element.string
                except TypeError:
                    continue
        directions.append(directions_text)
    return directions


def assemble_recipe(recipe_soup, title, recipe_link):
    recipe_photo = get_recipe_photo(recipe_soup)
    recipe_info = get_recipe_info(recipe_soup)

    found_blacklist = check_blacklist_words(title)

    if found_blacklist:
        return False

    try:
        recipe_yield, recipe_active_cooking_time, recipe_total_cooking_time = recipe_info
    except ValueError:
        return False

    try:
        ingredients_div = recipe_soup.find("div", attrs={"class": "tasty-recipes-ingredients"}).ul
    except AttributeError:
        return False

    ingredients = get_ingredients(ingredients_div)

    try:
        directions_div = recipe_soup.find("div", attrs={"class": "tasty-recipes-instructions"})
    except AttributeError:
        return False

    directions = get_directions(directions_div)

    if ingredients and directions and recipe_total_cooking_time:
        recipes.append({
            "title": title,
            "ingredients": ingredients,
            "directions": directions,
            "yield": recipe_yield,
            "active_time": recipe_active_cooking_time,
            "total_time": recipe_total_cooking_time,
            "photo_link": recipe_photo,
            "recipe_link": recipe_link
        })


def get_recipes(url_start, url_end, start_page=1, end_page=1):
    recipes_metadata = get_recipes_metadata(url_start, url_end, start_page, end_page)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(request_soup_and_assemble_recipe, recipes_metadata)
    return recipes


def request_soup_and_assemble_recipe(recipe):
    recipe_page = request("GET", recipe['recipe_link'])
    recipe_soup = BeautifulSoup(recipe_page.text, "lxml")
    assemble_recipe(recipe_soup, recipe['recipe_title'], recipe['recipe_link'])


if __name__ == "__main__":
    get_recipes("https://www.gimmesomeoven.com/all-recipes/?fwp_course=main-course&fwp_paged=",
                "&fwp_per_page=100&fwp_sort=date_desc", 5, 6)

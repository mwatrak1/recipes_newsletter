from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from prepare_email_content import generate_random_recipes


def create_email_with_recipes(sender_email, receiver_email, subject):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    part1 = render_text_email()
    part2 = render_recipes_html_email()

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message


def render_recipes_html_email():
    recipes = generate_random_recipes()
    styles = get_styles()
    meals_html = f"""
        <html>
            <head>{styles}</head>
            <body style="background-color: #4EB34D; border-radius: 25px;
                        border-color: #FFFFFF; padding: 2% 5% 2% 5%;
            ">
    """

    for meal, recipe in recipes.items():
        ingredients = render_ingredients(recipe["ingredients"])
        directions = render_directions(recipe["directions"])
        timers = render_cooking_times(recipe["active_time"], recipe["total_time"])

        meal_div = f"""\
            <p>
                <h2>{recipe["title"]}</h2>
                <h3>{meal.title()}</h3>
                <img src="{recipe['photo_link']}" 
                style="display: block; margin-left: auto; margin-right: auto;
                width: 70%; text-align:center; border-radius:15px;" alt="recipe photo">
                    {timers}
                    {ingredients}
                    {directions} 
                <div style="margin-top: 2%; margin-bottom: 6%; text-align: center;">
                    <h3>
                        <a href="{recipe["recipe_link"]}">
                            Check out this recipe ->
                        </a>
                    </h3>
                </div>
            </p>
        """
        meals_html += meal_div

    meals_html += """
            </body>
        </html>
    """
    return MIMEText(meals_html, "html")


def render_cooking_times(active_time, total_time):
    return f"""\
        <div class="timers" style="margin-top: 2%; text-align:center;">
            <b> Active Time:</b> {active_time} \t\t<b>Total Time:</b> {total_time}
        </div>
    """


def render_ingredients(ingredients_list):
    ingredients_list_html = render_html_list(ingredients_list)
    return f"""\
        <div class="ingredients" 
        style="display:inline-block;">
            <h3>Ingredients</h3>
            <ul>
                {ingredients_list_html}
            </ul>
        </div>
    """


def render_directions(directions_list):
    directions_list_html = render_html_list(directions_list)
    return f"""\
        <div class="directions" style="display:inline-block;">
            <h3>Directions</h3>
            <ol>
                {directions_list_html}
            </ol>
        </div>
    """


def render_html_list(list_items):
    html_list = ""
    for item in list_items:
        new_element_html = f"<li>{item}</li>\n"
        html_list += new_element_html
    return html_list


def get_styles():
    return """\
        <style>
            img {
                display: block;
            }
            
            .directions {
                
            }
            
            .ingredients {
                margin-left: 10px;
                display: inline-block;
            }
            
            .timers {
            
            }
        </style>
    """


def render_text_email():
    text = """\
        Text version not implemented
        """
    return MIMEText(text, "plain")

import smtplib
import ssl
from create_email import create_email_with_recipes
from prepare_email_content import get_users_emails
import os
from dotenv import load_dotenv

load_dotenv()

port = 465  # SSL
password = os.getenv("EMAIL_PASSWORD")
email_server = "recipes.newsletter@gmail.com"


def send_recipes(users_emails):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email_server, password)

        for users_email in users_emails:
            email_content = create_email_with_recipes(email_server, users_email, "Recipes for tomorrow")
            server.sendmail(email_server, users_email, email_content.as_string())


if __name__ == "__main__":
    all_users_emails = get_users_emails()
    send_recipes(all_users_emails)

import os
import smtplib
import ssl

import requests
import selectorlib
from dotenv import load_dotenv

# Load the variables from the .env file into your environment
load_dotenv()

URL = "https://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    """scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    # Pull credentials securely from the .env file
    username = os.getenv("EMAIL_USERNAME")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("RECEIVER")

    context = ssl.create_default_context()

    # The \n\n is strictly required by email servers to separate the Subject from the Body
    email_message = f"Subject: New Music Event Alert!\n\n{message}"

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, email_message)
    print("Email was sent!")


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    content = read(extracted)
    if extracted != "No upcoming tours" and extracted not in content:
        store(extracted)
        send_email(message="Hey, new event was found! Check it out!!")

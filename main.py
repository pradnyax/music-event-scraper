import os
import smtplib
import sqlite3
import ssl

import requests
import selectorlib
from dotenv import load_dotenv

# Load the variables from the .env file into your environment
load_dotenv()

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

# Establish global connection to the database
connection = sqlite3.connect("data.db")


def scrape(url):
    """scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
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
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row

    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date)
    )
    rows = cursor.fetchall()
    return rows


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(f"Website currently says: {extracted}")

    if extracted != "No upcoming tours":
        row = read(extracted)
        # If the database returns an empty list, it means this tour is new
        if not row:
            store(extracted)
            send_email(message=f"Hey, a new event was found!\n\nDetails: {extracted}")

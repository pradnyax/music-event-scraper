# 🎸 Music Event Scraper

An automated Python script that monitors a website for upcoming music tours and events. When a new tour is detected, the script logs the event details (Band, City, Date) into an SQLite database to prevent duplicate notifications and sends a secure email alert to the user.

## Features
* **Automated Web Scraping:** Uses `requests` and `selectorlib` to extract specific event data from raw HTML.
* **Database Memory:** Integrates `sqlite3` to store previously scraped events, ensuring duplicate emails are not sent for the same tour.
* **Secure Email Notifications:** Uses `smtplib` and `ssl` to send automated alerts.
* **Credential Protection:** Utilizes `python-dotenv` to keep sensitive email passwords and addresses hidden from version control.
* **Modern Environment Management:** Built using `uv` for lightning-fast dependency and virtual environment management.

## Tech Stack
* **Language:** Python
* **Libraries:** `requests`, `selectorlib`, `python-dotenv`, `smtplib`, `sqlite3`
* **Package Manager:** `uv`


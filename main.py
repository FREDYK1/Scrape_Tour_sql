import requests
import selectorlib
import ssl
import smtplib
import time
import sqlite3


URL = "https://programmer100.pythonanywhere.com/tours/"

# Set a connection to the database
connection = sqlite3.connect("data.db")

# Get the source code form the website URL
def scrape(url):
    response = requests.get(url)
    source = response.text
    return source

# Extract the information from the source code
def extractor(source):
    selector = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = selector.extract(source)["tours"]
    return value

# Email the user
def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    username = "frederickkankam7@gmail.com"
    password = "wieu tuab eelc uubr"
    receiver = "frederickkankam7@gmail.com"
    context = ssl.create_default_context()
    message_format = f"""\
Subject: New Tour Alert
From: {username}
{message}
"""

    with smtplib.SMTP_SSL(host,port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message_format.encode('utf-8'))

# Store the information in the database
def store(tour):
    tour = tour.split(",")
    tour = [tour.strip() for tour in tour]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES (?, ?, ?)", tour)
    connection.commit()

# Read the information from the database
def read(extract):
    tour = extract.split(",")
    tour = [tour.strip() for tour in tour]
    band, city, date = tour
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band = ? AND city = ? AND date = ?", (band, city, date))
    row = cursor.fetchall()
    return row



# A program to scrape a website for information on upcoming tours and send it to the user
if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extractor(scraped)
        print(extracted)
        if extracted != "No upcoming tours":
            Tours = read(extracted)
            if not Tours:
                store(extracted)
                send_email(extracted)
        time.sleep(2)
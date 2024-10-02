import requests
import selectorlib
import ssl
import smtplib
import time
import sqlite3

from example import cursor

URL = "https://programmer100.pythonanywhere.com/tours/"

connection = sqlite3.connect("data.db")


def scrape(url):
    response = requests.get(url)
    source = response.text
    return source


def extractor(source):
    selector = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = selector.extract(source)["tours"]
    return value

def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    username = "frederickkankam7@gmail.com"
    password = "wieu tuab eelc uubr"
    receiver = "frederickkankam7@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host,port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message.encode('utf-8'))


def store(tour):
    tour = tour.split(",")
    tour = [tour.strip() for tour in tour]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES (?, ?, ?)", tour)
    connection.commit()


def read(extracted):
    tour = extracted.split(",")
    tour = [tour.strip() for tour in tour]
    band, city, date = tour
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band = ? AND city = ? AND date = ?", (band, city, date))
    row = cursor.fetchall()
    return row




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
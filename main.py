import requests
import selectorlib
import ssl
import smtplib
import time
import sqlite3


URL = "https://programmer100.pythonanywhere.com/tours/"



# Create a Event Class to extract the event form source code
class Event:
    def scrape(self, url):
        response = requests.get(url)
        source = response.text
        return source

    # Extract the information from the source code
    def extractor(self, source):
        selector = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = selector.extract(source)["tours"]
        return value


# Create Class Email to send email to the user
class Email:
    def send(self, message):
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
class Database:
    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def store(self, tour):
        tour = tour.split(",")
        tour = [tour.strip() for tour in tour]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES (?, ?, ?)", tour)
        self.connection.commit()

    # Read the information from the database
    def read(self, extract):
        tour = extract.split(",")
        tour = [tour.strip() for tour in tour]
        band, city, date = tour
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band = ? AND city = ? AND date = ?", (band, city, date))
        row = cursor.fetchall()
        return row



# A program to scrape a website for information on upcoming tours and send it to the user
if __name__ == "__main__":
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extractor(scraped)
        print(extracted)
        if extracted != "No upcoming tours":
            database = Database(database_path="data.db")
            Tours = database.read(extracted)
            if not Tours:
                database.store(extracted)
                email = Email()
                email.send(extracted)
        time.sleep(2)
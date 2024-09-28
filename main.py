import requests
import selectorlib
import ssl
import smtplib

URL = "https://programmer100.pythonanywhere.com/tours/"


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
    print("Email was sent")


def store(tour):
    with open("Tours.txt", "a") as file:
        file.write(tour + '\n')


def read():
    with open("Tours.txt", "r") as file:
        return file.read()




if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extractor(scraped)
    Tours = read()
    print(extracted)
    if extracted != "No upcoming tours":
        if extracted not in Tours:
            store(extracted)
            send_email(extracted)

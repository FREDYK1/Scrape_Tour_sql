import requests
import selectorlib


URL = "https://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    response = requests.get(url)
    source = response.text
    return source


if __name__ == "__main__":
    print(scrape(URL))
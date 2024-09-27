import requests
import selectorlib


URL = "https://programmer100.pythonanywhere.com/tours/"


def scrape(url):
    response = requests.get(url)
    source = response.text
    return source


def extractor(source):
    selector = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = selector.extract(source)["tours"]
    return value


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extractor(scraped)
    print(extracted)
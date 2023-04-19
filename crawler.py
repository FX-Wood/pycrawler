import requests

def crawl():
    uri = "https://wikipedia.com/wiki/Microsoft"
    # get uri data
    data = requests.get(uri).text
    print(data)
    # parse html
    # count words in html
    # limit by section
    # allow excluding words


if __name__ == "__main__":
    crawl()

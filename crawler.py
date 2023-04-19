import requests
from bs4 import BeautifulSoup

def crawl():
    uri = "https://wikipedia.com/wiki/Microsoft"
    # get uri data
    data = requests.get(uri).text
    # parse html
    soup = BeautifulSoup(data, 'html.parser')
    section_headers = soup.find_all('h2')
    # limit by section
    history_header = section_headers[0]
    for header in section_headers:
        for child in header.contents:
            if "History" in child:
                history_header = header

    history_text_contents = []
    next_sibling = history_header.find_next_sibling()
    while True:
        # currently wikipedia uses h2s for section headings
        if 'h2' in next_sibling.name:
            break
        # don't parse style tags, captions, etc
        if 'p' in next_sibling.name:
            for string in next_sibling.stripped_strings:
                history_text_contents.append(string)
        next_sibling = next_sibling.find_next_sibling()

    print(history_text_contents)

    # count words in html
    # allow excluding words

if __name__ == "__main__":
    crawl()

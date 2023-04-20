import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import re

def filter_strings(strings: List[str]) -> List[str]:
    """filter out non-words from the soup output"""
    result = []
    for string in strings:
        # this is not great, for example it splits
        # "Traf-O-Data" and MS-DOS into multiple words
        # if hyphenated words are not common this has less
        # impact because we're usually interested in the most
        # common words
        words = re.findall(r'\w+', string)
        result.extend(words)
    return result

def count_words(words: List[str]) -> Dict:
    """given a list of words, count instances of each word. case-sensitive"""
    result = {}
    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
    return result

def crawl():
    """crawl a given page, for example a wikipedia page, and count words"""
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

    clean_text = filter_strings(history_text_contents)

    count = count_words(clean_text)
    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_count = {key: value for key, value in sorted(count.items(), key=lambda item: item[1], reverse=True)}
    export_data = list(sorted_count.items())[:10]
    print(export_data)
    # count words in html
    # allow excluding words

if __name__ == "__main__":
    crawl()

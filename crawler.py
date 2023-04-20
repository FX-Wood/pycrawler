import typer
import requests
from bs4 import BeautifulSoup
import re

def filter_strings(strings: list[str]) -> list[str]:
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

def count_words(words: list[str]) -> dict:
    """given a list of words, count instances of each word. case-sensitive"""
    result = {}
    for word in words:
        if word in result:
            result[word] += 1
        else:
            result[word] = 1
    return result

def export_data(data: list[tuple[str, int]]):
    print(data)

def process_html(html_data: str) -> dict[str, int]:
    """takes a string of html and returns a dict with a wordcount"""
    # parse html
    soup = BeautifulSoup(html_data, 'html.parser')
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
        # don't save style tags, captions, etc
        if 'p' in next_sibling.name:
            for string in next_sibling.stripped_strings:
                history_text_contents.append(string)
        next_sibling = next_sibling.find_next_sibling()

    clean_text = filter_strings(history_text_contents)

    # count words in html
    count = count_words(clean_text)
    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_count = {key: value for key, value in sorted(count.items(), key=lambda item: item[1], reverse=True)}
    return sorted_count

def exclude_words(counted_words: dict[str,int], excludes_list: list[str]) -> dict[str,int]:
    """mutate input word count by removing some words"""
    for word in excludes_list:
        counted_words.pop(word, None)
    return counted_words
    

def crawl(top: int, excludes: list[str]):
    """crawl a given page, for example a wikipedia page, and count words"""
    assert top > 0, "must return at least one wordcount"
    uri = "https://wikipedia.com/wiki/Microsoft"
    # get uri data
    data = requests.get(uri).text

    counted_words = process_html(data)
    # allow excluding words
    exclude_words(counted_words, excludes)
    output_data = list(counted_words.items())
    
    # allow arbitrary number of top words
    if len(output_data) < top:
        export_data(output_data)
    else:
        export_data(output_data[:top])

def main(top: int, excludes: list[str]):
    print(f'{top},{excludes}')
    crawl(top, excludes)

if __name__ == "__main__":
    typer.run(main)

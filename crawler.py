import typer
from rich.console import Console
from rich.table import Table
import requests
from bs4 import BeautifulSoup, element
import re

def filter_strings(strings: list[str]) -> list[str]:
    """filter out non-words from the soup output"""
    result = []
    for string in strings:
        # https://stackoverflow.com/questions/31910955/regex-to-match-words-with-hyphens-and-or-apostrophes
        #words = re.findall(r"(?=\S*['-])([a-zA-Z'-]+)", string)
        words = re.findall(r"\b[a-zA-Z]+(?:['-]?[a-zA-Z]+)*\b", string)
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
    """use 'rich' library to print to console"""
    table = Table(title=f'Top {len(data)} Words')
    table.add_column("Word", style="green")
    table.add_column("Count", style="yellow")
    for item in data:
        table.add_row(item[0], str(item[1]))
    console = Console()
    console.print(table)

def get_section_header(filter: str, html_data) -> element.Tag:
    # parse html
    soup = BeautifulSoup(html_data, 'html.parser')
    section_headers = soup.find_all('h2')
    # limit by section
    for header in section_headers:
        for child in header.contents:
            if filter in child:
                return header
    raise LookupError()



def process_html(filter: str, html_data: str) -> dict[str, int]:
    """takes a string of html and returns a dict with a wordcount"""
    try:
        target_header = get_section_header(filter, html_data)
    except LookupError:
        print(f'Section header {filter} not found')
        exit()

    section_contents = []
    next_sibling = target_header.find_next_sibling()
    while True:
        if next_sibling is None:
            break
        # currently wikipedia uses h2s for section headings
        if 'h2' in next_sibling.name:
            break
        # don't save style tags, captions, etc
        if 'p' in next_sibling.name:
            for string in next_sibling.stripped_strings:
                section_contents.append(string)
        next_sibling = next_sibling.find_next_sibling()

    clean_text = filter_strings(section_contents)

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
    filter = "History"
    # get uri data
    data = requests.get(uri).text

    counted_words = process_html(filter, data)
    # allow excluding words
    exclude_words(counted_words, excludes)
    output_data = list(counted_words.items())
    
    # allow arbitrary number of top words
    if len(output_data) < top:
        export_data(output_data)
    else:
        export_data(output_data[:top])

def main(
        top: int = typer.Argument(10, help="try '5' (without the quotes)"),
        excludes: list[str] = typer.Argument(None, help="try 'a' 'of' 'in'"),
    ):
    """
    crawl the microsoft page of wikipedia
    and get the top n most frequently used 
    words of the history section

    for example:
    python crawler.py 10 "the" "of" "Microsoft"
    """
    crawl(top, excludes)

if __name__ == "__main__":
    typer.run(main)

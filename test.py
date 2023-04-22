import unittest
from pathlib import Path
from crawler import crawl, exclude_words, filter_strings, get_section_header

class TestCrawl(unittest.TestCase):
    def test_top_too_low(self):
        with self.assertRaises(AssertionError):
            crawl(0, [])

class TestFilterStrings(unittest.TestCase):
    def test_good_words(self):
        goodData = [
            'Childhood friends',
            'Bill Gates',
            'and',
            'Paul Allen',
            'sought to make a business using their skills in',
            'computer programming',
        ]
        result = filter_strings(goodData)
        
        assert len(result) == 18, f'filter is returning {"too many" if len(result) > 18 else "too few"}'
    
    def test_hyphenated(self):
        result = filter_strings(["asdf","Traf-O-Data","blitzes MS-DOS"])
        assert len(result) == 4, f'need to handle hyphenated words, {result}'

    def test_contractions(self):
        result = filter_strings(["asdf","it's","they're","manakin skywalker ain't"])
        assert len(result) == 6, f'need to handle contractions {result}'

    def test_single_letters(self):
        result = filter_strings(["a brown cow", "jumped", "over the moon"])
        assert len(result) == 7, f'need to handle single letters, {result}'

class TestExcludeWords(unittest.TestCase):
    def test_single_word(self):
        data = {
            "asdf": 10,
            "lkj": 3,
            "hello": 1,
        }
        filtered_data = exclude_words(data, ["hello"])
        print(data.keys())
        assert "hello" not in filtered_data, "excluded word was not excluded"

class TestGetSectionHeader(unittest.TestCase):
    html_data = """
            <h2><span class="mw-headline" id="Corporate_identity">Corporate identity</span></h2>
            <h2><span class="mw-headline" id="History">History</span></h2>'
            <h2><span class="mw-headline" id="Corporate_affairs">Corporate affairs</span></h2>
        """
    def test_gets_history_header(self):
        result = get_section_header("History", self.html_data)
        assert "History" in result.strings, "couldn't find correct header"

    def test_raises_for_header_not_found(self):
        with self.assertRaises(LookupError):
            get_section_header("Farfetched", self.html_data)

if __name__ == '__main__':
    unittest.main()


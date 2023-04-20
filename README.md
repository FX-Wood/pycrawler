# Pycrawler

Pycrawler is a sample app designed to meet the requirements of a coding challenge. The requirements are as follows:

>The code should return the most common words used and the number of times they are used. The following should be configurable:
>- The number of words to return (default: 10)
>- Words to exclude from the search

>The page to crawl:
>    https://en.wikipedia.org/wiki/Microsoft
> Only words from the section “history” should be accounted for

## Getting Started
### Docker
To run this application try the following:

1. `git clone https://github.com/fx-wood/pycrawler`
2. `cd pycrawler`
3. `docker build . -t pycrawler-fxwood`
4. `docker run pycrawler-fxwood`

To pass different arguments modify the docker run command:

`docker run -t pycrawler-fxwood 20`

`docker run -t pycrawler-fxwood 20 "the" "to" "of" "a" "and" "in" "for" "with" "On" "In"`

### Shell
To run this application in your shell try the following:
1. optionally use a venv
2. `git clone https://github.com/fx-wood/pycrawler`
3. `cd pycrawler`
4. `pip install -r requirements.txt`
5. `python3 crawler.py`

To modify the output change the arguments:

`python3 crawler.py 20`

`python3 crawler.py 8 "the" "to" "of" "a" "and" "in" "for" "with" "On" "In"`



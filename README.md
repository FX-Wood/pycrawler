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
3. `docker build . -t pycrawler-fxwood && docker run pycrawler-fxwood 10`

To pass different arguments modify the docker run command:
`docker run -t pycrawler-fxwood 20`
`docker run -t pycrawler-fxwood 20 "the" "to" "of" "a" "and" "in" "for" "with" "On" "In"`



FROM python:alpine3.17
WORKDIR /pycrawler
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python3", "crawler.py"]
CMD ["10", "the","On","to","of"]

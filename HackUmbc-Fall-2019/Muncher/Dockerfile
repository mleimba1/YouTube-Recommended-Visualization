FROM python:3

WORKDIR /opt

COPY requirements.txt .
COPY scrapy.cfg .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "scrapy", "crawl", "youtube" ]

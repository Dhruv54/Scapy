import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime

client = MongoClient("mongodb+srv://username:password@mycluster.qwert.mongodb.net/")    # connection string
db = client.scrapy

def insertToDB(page,title,rating,img,price,instock):
    collection = db[page]
    doc = { "title":title,
            "rating":rating,
            "img":img,
            "price":price,
            "instock":instock,
            "date":datetime.datetime.utcnow()
        }
    inserted = collection.insert_one(doc)
    return inserted.inserted_id

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"bokks-{page}.html"
        bookdetails={}
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")

        cards = response.css(".product_pod")

        for card in cards:
            title = card.css("h3>a::text").get()
            print(title)
            rating = card.css(".star-rating").attrib["class"].split(" ")[1]
            print(rating)
            img = card.css(".image_container img")
            img = img.attrib["src"].replace("../../../../media","https://books.toscrape.com/media")
            print(img)
            price = card.css(".price_color::text").get()
            print(price)
            availability = card.css(".instock")
            if len(availability.css(".icon-ok")) > 0:
                instock=True
            else:
                instock=False
            print(instock)

            insertToDB(page,title,rating,img,price,instock)

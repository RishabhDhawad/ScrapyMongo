from pymongo import MongoClient
import datetime

client = MongoClient("mongodb+srv://test:Password@1@scrapy.kxqfcyt.mongodb.net/")

db = client.scrapy

posts = db.test_collection

doc = post = {"author": "Mike",
              "text": "My first blog post!",
              "tags": ["mongodb", "python", "pymongo"],
              "date": datetime.datetime.utcnow()}

post_id = posts.insert_one(post).inserted_id


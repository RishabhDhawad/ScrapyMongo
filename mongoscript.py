from pymongo import MongoClient
import datetime
import os

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI environment variable is not set")

client = MongoClient(MONGODB_URI)
db = client.scrapy

posts = db.test_collection

post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow(),
}

post_id = posts.insert_one(post).inserted_id

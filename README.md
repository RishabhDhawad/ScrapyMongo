# BooksData: Scrapy + MongoDB

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Scrapy](https://img.shields.io/badge/Scrapy-Framework-60A839?logo=scrapy&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)

> Scrapes book listings from Books to Scrape and stores results in MongoDB Atlas.

---

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [MongoDB Configuration](#mongodb-configuration)
- [Running the Spider](#running-the-spider)
- [Data Model](#data-model)
- [Quick Mongo Test](#quick-mongo-test)
- [Troubleshooting](#troubleshooting)
- [Notes](#notes)

## Overview
- **Spider**: `booksdata/spiders/books.py` (name: `books`)
- **Targets**:
  - https://books.toscrape.com/catalogue/category/books/travel_2/index.html
  - https://books.toscrape.com/catalogue/category/books/mystery_3/index.html
- **Storage**: Each page/category is saved to a MongoDB collection named after the URL segment (e.g., `travel_2`, `mystery_3`).
- **Fields saved**: `title`, `rating`, `image`, `price`, `inStock`, `date` (UTC).
- **Example Mongo script**: `mongoscript.py` inserts a sample document.

## Project Structure
- `booksdata/` Scrapy project package
  - `spiders/books.py` Spider implementation
- `mongoscript.py` Quick MongoDB insert example
- `README.md` This file

## Requirements
- Python 3.9+
- Packages: `scrapy`, `pymongo`, `dnspython`

Install dependencies:
```bash
pip install scrapy pymongo dnspython
```

## MongoDB Configuration
The code connects to MongoDB via a connection string in both `books.py` and `mongoscript.py`:
```python
MongoClient("mongodb+srv://<user>:<password>@<cluster-host>/<options>")
```

Replace the placeholder credentials/host with your own. If using MongoDB Atlas, ensure your IP is allowlisted and SRV is enabled.

Tip: Prefer using an environment variable and load it in code, e.g. `MONGODB_URI`.

## Running the Spider
From the project root:
```bash
scrapy crawl books
```

Data will be inserted into the `scrapy` database, with collections named by page (e.g., `travel_2`).

## Data Model
Documents inserted by the spider look like:
```json
{
  "title": "Book Title",
  "rating": "Three",
  "image": "https://books.toscrape.com/media/...",
  "price": "£23.88",
  "inStock": true,
  "date": "2025-01-01T00:00:00Z"
}
```

## Quick Mongo Test
Run the sample script:
```bash
python mongoscript.py
```
This inserts a test document into `test_collection` in the `scrapy` database.

## Troubleshooting
- If the spider starts but does not fetch the category pages, ensure the entry method is correct. Scrapy calls `start_requests()` by default. If needed, rename the async `start` method in `books.py` to `start_requests` (and remove `async`).
- Connection errors to MongoDB Atlas: verify connection string, credentials, network/IP allowlist, and that `dnspython` is installed for SRV URIs.
- SSL/DNS issues on Windows: update `certifi` (`pip install -U certifi`) and ensure system time is correct.

## Notes
- The image URL is normalized to absolute path for `books.toscrape.com` media.
- Collections are per-category page; adjust if you prefer a single collection.


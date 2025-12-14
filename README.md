# BooksData: Scrapy + MongoDB + HTML Export

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Scrapy](https://img.shields.io/badge/Scrapy-Framework-60A839?logo=scrapy&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)

> Scrapes book listings from Books to Scrape, stores results in MongoDB Atlas, and generates formatted HTML tables.

---

## Table of Contents
- [Quick Start](#quick-start)
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [MongoDB Configuration](#mongodb-configuration)
- [Running the Spider](#running-the-spider)
- [HTML Output](#html-output)
- [Data Model](#data-model)
- [Utility Scripts](#utility-scripts)
- [Troubleshooting](#troubleshooting)
- [Notes](#notes)

## Quick Start
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure MongoDB:**
   - Update the connection string in `booksdata/spiders/books.py` and `mongoscript.py`
   - Replace `mongodb+srv://test:Password@scrapymongo.n15gpxm.mongodb.net` with your MongoDB Atlas connection string

3. **Run the spider:**
   ```bash
   scrapy crawl books
   ```

4. **Check results:**
   - MongoDB: Data saved in `scrapy` database
   - HTML files: `books-travel.html` and `books-mystery.html` in project root

## Overview
- **Spider**: `booksdata/spiders/books.py` (name: `books`)
- **Targets**:
  - https://books.toscrape.com/catalogue/category/books/travel_2/index.html
  - https://books.toscrape.com/catalogue/category/books/mystery_3/index.html
- **Storage**: 
  - MongoDB: Each page/category is saved to a MongoDB collection named after the URL segment (e.g., `travel`, `mystery`)
  - HTML Files: Formatted HTML tables are generated automatically (e.g., `books-travel.html`, `books-mystery.html`)
- **Fields scraped**: `title`, `rating`, `image`, `price`, `inStock`, `date` (UTC)

## Features
- ✅ Web scraping with Scrapy framework
- ✅ MongoDB Atlas integration for data persistence
- ✅ Automatic HTML table generation from scraped data
- ✅ Standalone HTML formatter utility for existing HTML files
- ✅ Full title extraction with fallback mechanisms
- ✅ Image handling with placeholder support
- ✅ Responsive table design

## Project Structure
```
booksdata/
├── booksdata/              # Scrapy project package
│   ├── spiders/
│   │   └── books.py        # Main spider implementation
│   ├── items.py            # Scrapy items definition
│   ├── pipelines.py       # Data processing pipelines
│   ├── middlewares.py      # Request/response middlewares
│   └── settings.py         # Scrapy settings
├── format_books_table.py   # Standalone HTML formatter utility
├── mongoscript.py          # MongoDB connection test script
├── requirements.txt        # Python dependencies
├── scrapy.cfg             # Scrapy configuration
└── README.md              # This file
```

## Requirements
- Python 3.9+
- Required packages (see `requirements.txt`):
  - `scrapy>=2.11.0` - Web scraping framework
  - `pymongo>=4.6.0` - MongoDB driver
  - `itemadapter>=0.7.0` - Scrapy item adapter
  - `parsel>=1.8.0` - HTML/XML parsing library

## Installation
1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install scrapy pymongo itemadapter parsel
```

## MongoDB Configuration
The code connects to MongoDB via a connection string in both `books.py` and `mongoscript.py`:
```python
MongoClient("mongodb+srv://<user>:<password>@<cluster-host>/<options>")
```

**Important**: Replace the placeholder credentials/host with your own MongoDB Atlas connection string. If using MongoDB Atlas, ensure:
- Your IP address is allowlisted in the Atlas network settings
- SRV connection is enabled
- Username and password are properly URL-encoded (special characters like `@` must be encoded)

**Security Tip**: Prefer using an environment variable and load it in code, e.g. `MONGODB_URI`, instead of hardcoding credentials.

## Running the Spider
From the project root:
```bash
scrapy crawl books
```

**What happens:**
1. Spider scrapes book data from the target URLs
2. Data is saved to MongoDB (`scrapy` database, collections: `travel`, `mystery`)
3. HTML table files are automatically generated in the project root:
   - `books-travel.html`
   - `books-mystery.html`

## HTML Output
The spider automatically generates formatted HTML tables containing:
- Book cover images (with fallback placeholders)
- Full book titles
- Star ratings
- Prices
- Stock availability status

**HTML File Format:**
- Simple, clean table design
- Responsive layout
- Alternating row colors for readability
- Images displayed as thumbnails (80x120px)

**Example output files:**
- `books-travel.html` - Travel books category
- `books-mystery.html` - Mystery books category

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

## Utility Scripts

### MongoDB Connection Test
Test your MongoDB connection:
```bash
python mongoscript.py
```
This inserts a test document into `test_collection` in the `scrapy` database.

### HTML Formatter Utility
Reformat existing HTML files into styled tables:
```bash
python format_books_table.py <input_html> [output_html]
```

**Examples:**
```bash
# Format a file and create output with _table suffix
python format_books_table.py books-travel.html

# Specify custom output filename
python format_books_table.py books-travel.html formatted-travel.html
```

**Features:**
- Parses HTML files containing book listings
- Generates styled HTML tables with modern design
- Supports dark mode
- Handles image URL normalization

## Troubleshooting

### Spider Issues
- **Spider doesn't start**: The spider uses an `async def start()` method. If Scrapy doesn't recognize it, ensure you're using Scrapy 2.11+ or rename it to `start_requests()` (and remove `async`).
- **No data scraped**: Check that the target URLs are accessible and the CSS selectors in `books.py` match the website structure.

### MongoDB Issues
- **Connection errors**: 
  - Verify your MongoDB connection string is correct
  - Ensure credentials are properly URL-encoded (use `urllib.parse.quote_plus()` for special characters)
  - Check that your IP is allowlisted in MongoDB Atlas
  - Verify `pymongo` is installed: `pip install pymongo`
- **SSL/DNS issues on Windows**: 
  - Update certificates: `pip install -U certifi`
  - Ensure system time is correct
  - Check firewall settings

### HTML Generation Issues
- **HTML files not created**: Check that the spider successfully scraped data (books_data list is not empty)
- **Images not displaying**: Verify image URLs are absolute (the spider converts relative URLs automatically)
- **Title extraction issues**: The spider tries multiple methods (text content, title attribute) to extract full titles

## Notes
- **Image URLs**: Automatically normalized to absolute paths for `books.toscrape.com` media
- **Collections**: Each category page creates its own MongoDB collection (e.g., `travel`, `mystery`)
- **Title Extraction**: The spider uses fallback mechanisms to ensure full titles are captured:
  1. First tries `h3>a::text`
  2. Falls back to `h3>a::attr(title)` if text is empty
  3. Defaults to "No Title Available" if both fail
- **HTML Files**: Generated in the project root directory with naming pattern `books-{category}.html`
- **Database**: All data is stored in the `scrapy` database in MongoDB


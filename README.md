# 📚 BooksData

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Scrapy](https://img.shields.io/badge/Scrapy-Framework-60A839?logo=scrapy&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?logo=mongodb&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)

> Scrapes book listings from Books to Scrape, stores results in MongoDB Atlas, and generates formatted HTML tables.

**A powerful web scraping tool that extracts book listings, stores them in MongoDB, and generates beautiful HTML tables**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Troubleshooting](#-troubleshooting)

</div>

---

## 🎯 Overview

**BooksData** is a comprehensive web scraping solution built with Scrapy that:

- 🕷️ **Scrapes** book data from [Books to Scrape](https://books.toscrape.com)
- 💾 **Stores** data in MongoDB Atlas for persistence
- 📊 **Generates** beautifully formatted HTML tables automatically
- 🛠️ **Provides** utility tools for data formatting and testing

### 🎨 What You Get

```
┌─────────────────────────────────────────────────────────┐
│  📥 Scraped Data  →  💾 MongoDB  →  📄 HTML Tables     │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🕷️ **Web Scraping** | Powerful Scrapy framework for efficient data extraction |
| 💾 **MongoDB Integration** | Seamless data persistence with MongoDB Atlas |
| 📊 **HTML Generation** | Automatic creation of formatted HTML tables |
| 🎨 **Beautiful Tables** | Clean, responsive design with image thumbnails |
| 🔄 **Standalone Utilities** | Additional tools for HTML formatting |
| 🛡️ **Error Handling** | Robust title extraction with fallback mechanisms |
| 🖼️ **Image Support** | Automatic image URL normalization and placeholders |
| 📱 **Responsive Design** | Tables that work on all screen sizes |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- MongoDB Atlas account (or local MongoDB instance)

### Installation Steps

<details>
<summary><b>📦 Step 1: Install Dependencies</b></summary>

```bash
# Clone or download the repository
git clone <repository-url>
cd booksdata

# Install all dependencies
pip install -r requirements.txt
```

**Or install manually:**
```bash
pip install scrapy pymongo itemadapter parsel
```
</details>

<details>
<summary><b>⚙️ Step 2: Configure MongoDB</b></summary>

1. Update the connection string in:
   - `booksdata/spiders/books.py`
   - `mongoscript.py`

2. Replace the placeholder:
   ```python
   # Before
   MongoClient("mongodb+srv://test:Password@scrapymongo.n15gpxm.mongodb.net")
   
   # After (use your own credentials)
   MongoClient("mongodb+srv://your_user:your_password@your_cluster.mongodb.net")
   ```

3. **Security Tip** 💡: Use environment variables instead of hardcoding:
   ```python
   import os
   MongoClient(os.getenv("MONGODB_URI"))
   ```
</details>

<details>
<summary><b>▶️ Step 3: Run the Spider</b></summary>

```bash
scrapy crawl books
```

**Expected Output:**
```
✅ Scraping books from travel...
✅ Scraping books from mystery...
✅ Data saved to MongoDB
✅ HTML files generated: books-travel.html, books-mystery.html
```
</details>

<details>
<summary><b>📊 Step 4: Check Results</b></summary>

**MongoDB:**
- Database: `scrapy`
- Collections: `travel`, `mystery`

**HTML Files:**
- `books-travel.html` - Travel books category
- `books-mystery.html` - Mystery books category
</details>

---

## 📖 Documentation

### 🎯 Target URLs

The spider scrapes data from:

- 📍 `https://books.toscrape.com/catalogue/category/books/travel_2/index.html`
- 📍 `https://books.toscrape.com/catalogue/category/books/mystery_3/index.html`

### 📁 Project Structure

```
booksdata/
│
├── 📂 booksdata/              # Scrapy project package
│   ├── 📂 spiders/
│   │   └── 📄 books.py        # Main spider implementation
│   ├── 📄 items.py            # Scrapy items definition
│   ├── 📄 pipelines.py        # Data processing pipelines
│   ├── 📄 middlewares.py      # Request/response middlewares
│   └── 📄 settings.py         # Scrapy settings
│
├── 📄 format_books_table.py   # Standalone HTML formatter utility
├── 📄 mongoscript.py          # MongoDB connection test script
├── 📄 requirements.txt        # Python dependencies
├── 📄 scrapy.cfg              # Scrapy configuration
└── 📄 README.md               # This file
```

### 📦 Requirements

| Package | Version | Purpose |
|---------|---------|---------|
| `scrapy` | >=2.11.0 | Web scraping framework |
| `pymongo` | >=4.6.0 | MongoDB driver |
| `itemadapter` | >=0.7.0 | Scrapy item adapter |
| `parsel` | >=1.8.0 | HTML/XML parsing library |

### 💾 Data Model

Each document stored in MongoDB follows this structure:

```json
{
  "title": "It's Only the Himalayas",
  "rating": "Two",
  "image": "https://books.toscrape.com/media/cache/...",
  "price": "£45.17",
  "inStock": true,
  "date": "2025-01-15T10:30:00Z"
}
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `title` | String | Full book title |
| `rating` | String | Star rating (One, Two, Three, Four, Five) |
| `image` | String | Absolute URL to book cover image |
| `price` | String | Book price with currency symbol |
| `inStock` | Boolean | Availability status |
| `date` | DateTime | UTC timestamp of when data was scraped |

---

## 🎨 HTML Output

The spider automatically generates beautifully formatted HTML tables with:

### ✨ Features

- 🖼️ **Book Cover Images** - Thumbnail images (80x120px) with fallback placeholders
- 📝 **Full Titles** - Complete book titles with proper HTML escaping
- ⭐ **Star Ratings** - Formatted rating display
- 💰 **Prices** - Currency-formatted prices
- 📦 **Stock Status** - Clear in-stock/out-of-stock indicators

### 📄 Example Output

```html
<!-- Generated file: books-travel.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Travel Books</title>
    <!-- Beautiful styling included -->
  </head>
  <body>
    <h1>Travel Books</h1>
    <table>
      <!-- Responsive table with all book data -->
    </table>
  </body>
</html>
```

### 🎯 Table Design

- ✅ Clean, modern design
- ✅ Alternating row colors
- ✅ Responsive layout
- ✅ Hover effects
- ✅ Professional typography

---

## 🛠️ Utility Scripts

### 🧪 MongoDB Connection Test

Test your MongoDB connection before running the spider:

```bash
python mongoscript.py
```

**What it does:**
- ✅ Connects to MongoDB Atlas
- ✅ Inserts a test document
- ✅ Verifies connection is working

**Expected Output:**
```
✅ Connected to MongoDB
✅ Test document inserted: <ObjectId>
```

### 📊 HTML Formatter Utility

Reformat existing HTML files into styled tables:

```bash
python format_books_table.py <input_html> [output_html]
```

**Usage Examples:**

```bash
# Basic usage - creates output with _table suffix
python format_books_table.py books-travel.html
# Output: books-travel_table.html

# Custom output filename
python format_books_table.py books-travel.html formatted-travel.html

# Format multiple files
python format_books_table.py books-travel.html
python format_books_table.py books-mystery.html
```

**Features:**
- 🎨 Modern, styled HTML tables
- 🌙 Dark mode support
- 🖼️ Image URL normalization
- 📱 Responsive design

---

## 🔧 Troubleshooting

### 🕷️ Spider Issues

<details>
<summary><b>Spider doesn't start</b></summary>

**Problem:** The spider uses `async def start()` method.

**Solution:**
- Ensure you're using Scrapy 2.11+
- Or rename to `start_requests()` and remove `async`:

```python
# Change this:
async def start(self):
    # ...

# To this:
def start_requests(self):
    # ...
```
</details>

<details>
<summary><b>No data scraped</b></summary>

**Checklist:**
- ✅ Target URLs are accessible
- ✅ CSS selectors match website structure
- ✅ Network connection is working
- ✅ Website hasn't changed structure

**Debug:**
```bash
scrapy crawl books -L DEBUG
```
</details>

### 💾 MongoDB Issues

<details>
<summary><b>Connection errors</b></summary>

**Common Issues:**

1. **Invalid Connection String**
   ```python
   # ❌ Wrong
   MongoClient("mongodb+srv://user:pass@cluster")
   
   # ✅ Correct (URL-encoded)
   from urllib.parse import quote_plus
   user = quote_plus("your_user")
   passwd = quote_plus("your_password")
   MongoClient(f"mongodb+srv://{user}:{passwd}@cluster")
   ```

2. **IP Not Allowlisted**
   - Go to MongoDB Atlas → Network Access
   - Add your current IP address
   - Or use `0.0.0.0/0` for development (not recommended for production)

3. **Missing Dependencies**
   ```bash
   pip install pymongo dnspython
   ```
</details>

<details>
<summary><b>SSL/DNS issues on Windows</b></summary>

**Solutions:**
```bash
# Update certificates
pip install -U certifi

# Verify system time is correct
# Check firewall settings
```
</details>

### 📄 HTML Generation Issues

<details>
<summary><b>HTML files not created</b></summary>

**Possible Causes:**
- Spider didn't scrape any data
- `books_data` list is empty
- File permissions issue

**Debug:**
```python
# Check logs for:
self.log(f"Generated HTML file: {output_path}")
```
</details>

<details>
<summary><b>Images not displaying</b></summary>

**Check:**
- ✅ Image URLs are absolute (not relative)
- ✅ URLs are accessible
- ✅ Browser console for 404 errors

**The spider automatically converts relative URLs:**
```python
if image:
    image = response.urljoin(image)  # Converts to absolute URL
```
</details>

---

## 📝 Notes

### 🔍 Title Extraction

The spider uses a **three-tier fallback system**:

1. **Primary:** `h3>a::text` - Extracts text content
2. **Fallback:** `h3>a::attr(title)` - Uses title attribute
3. **Default:** `"No Title Available"` - If both fail

### 🖼️ Image Handling

- **Automatic normalization** to absolute URLs
- **Placeholder support** for missing images
- **Base URL:** `https://books.toscrape.com/media/`

### 💾 Database Structure

```
scrapy (database)
├── travel (collection)
│   ├── {book documents}
│   └── ...
└── mystery (collection)
    ├── {book documents}
    └── ...
```

### 📄 File Naming

HTML files follow the pattern: `books-{category}.html`

**Examples:**
- `books-travel.html`
- `books-mystery.html`

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ using Scrapy, MongoDB, and Python**

⭐ Star this repo if you find it useful!

</div>

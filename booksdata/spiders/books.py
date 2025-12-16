import scrapy
from pathlib import Path
from pymongo import MongoClient
import datetime
import os

client = MongoClient("mongodb+srv://test:Password@scrapymongo.n15gpxm.mongodb.net")
db = client.scrapy

def insertToDb(page, title, rating, image, price, inStock):
    collection = db[page]
    doc = {"title": title, 
           "rating": rating, 
           "image": image, 
           "price": price, 
           "inStock": inStock, 
           "date": datetime.datetime.utcnow()}
    inserted = collection.insert_one(doc)
    return inserted.inserted_id

def generate_html_from_results(books_data, page_name, output_filename):
    """
    Convert scraped book results into a simple HTML table.
    
    Args:
        books_data: List of dictionaries containing book information
                    Each dict should have: title, rating, image, price, inStock
        page_name: Name of the page/category (e.g., 'travel_2', 'mystery_3')
        output_filename: Name of the output HTML file
    """
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Books - {page_name.replace('_', ' ').title()}</title>
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .book-image {{
            width: 80px;
            height: 120px;
            object-fit: cover;
            border-radius: 4px;
        }}
        td:nth-child(2) {{
            max-width: 500px;
            word-wrap: break-word;
            white-space: normal;
        }}
    </style>
</head>
<body>
    <h1>{page_name.replace('_', ' ').title()} Books</h1>
    <table>
        <thead>
            <tr>
                <th>Image</th>
                <th>Title</th>
                <th>Rating</th>
                <th>Price</th>
                <th>In Stock</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for book in books_data:
        title = book.get('title', 'N/A')
        rating = book.get('rating', 'N/A')
        image = book.get('image', '')
        price = book.get('price', 'N/A')
        in_stock = 'Yes' if book.get('inStock', False) else 'No'
        
        # Format rating display
        rating_display = rating.replace('_', ' ').title() if rating != 'N/A' else 'N/A'
        
        # Handle image - use placeholder if no image
        image_html = f'<img src="{image}" alt="{title}" class="book-image" onerror="this.src=\'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2280%22 height=%22120%22%3E%3Crect fill=%22%23ddd%22 width=%2280%22 height=%22120%22/%3E%3Ctext fill=%22%23999%22 font-family=%22sans-serif%22 font-size=%2212%22 dy=%2210.5%22 font-weight=%22bold%22 x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22%3ENo Image%3C/text%3E%3C/svg%3E\';">' if image else '<span>No Image</span>'
        
        html_content += f"""            <tr>
                <td>{image_html}</td>
                <td>{title}</td>
                <td>{rating_display}</td>
                <td>{price}</td>
                <td>{in_stock}</td>
            </tr>
"""
    
    html_content += f"""        </tbody>
    </table>
    <p>Total Books: {len(books_data)}</p>
</body>
</html>"""
    
    # Write to file
    output_path = Path(output_filename)
    output_path.write_text(html_content, encoding='utf-8')
    return output_path

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]
    
    async def start(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        books_data = []
        
        self.log(f"Parsing page: {page}")
        cards = response.css(".product_pod")
        
        for card in cards:
            # Extract full title - try text first, then title attribute
            title = card.css("h3>a::text").get()
            if not title or title.strip() == "":
                # If text is empty, try the title attribute
                title = card.css("h3>a::attr(title)").get()
            if not title:
                title = "No Title Available"
            # Clean up the title - strip whitespace
            title = title.strip() if title else "No Title Available"
            
            rating = card.css(".star-rating").attrib["class"].split(" ")[1]
            
            image = card.css("img::attr(src)").get()
            if image:
                image = response.urljoin(image)
            
            price = card.css(".price_color::text").get()
            
            availability = card.css(".availability")
            if len(availability.css(".icon-ok")) > 0:
                inStock = True
            else:
                inStock = False
            
            # Store book data for HTML generation
            book_data = {
                "title": title,
                "rating": rating,
                "image": image,
                "price": price,
                "inStock": inStock
            }
            books_data.append(book_data)
            
            # Insert to database
            insertToDb(page, title, rating, image, price, inStock)
        
        # Generate HTML file from scraped results
        if books_data:
            output_path = generate_html_from_results(books_data, page, filename)
            self.log(f"Generated HTML file: {output_path}")
        else:
            self.log(f"No books found on page: {page}")
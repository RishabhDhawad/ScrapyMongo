import sys
from pathlib import Path
from urllib.parse import urljoin
from parsel import Selector

BASE_MEDIA = "https://books.toscrape.com/media/"

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>
    :root { color-scheme: light dark; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
           Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', Arial, sans-serif;
           margin: 24px; }
    h1 { margin: 0 0 16px; font-size: 1.8rem; }
    .meta { margin: 0 0 20px; color: #777; font-size: .95rem; }
    table { width: 100%; border-collapse: collapse; border: 1px solid #e2e8f0; }
    thead th { position: sticky; top: 0; background: #f8fafc; text-align: left; }
    th, td { padding: 10px 12px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }
    tbody tr:hover { background: #f1f5f9; }
    .price { font-weight: 600; }
    .rating { display: inline-block; padding: 2px 8px; border-radius: 999px; background: #e2e8f0; font-size: .85rem; }
    .instock { color: #16a34a; font-weight: 600; }
    .outstock { color: #dc2626; font-weight: 600; }
    .img { display: flex; align-items: center; gap: 10px; }
    img { width: 48px; height: 72px; object-fit: cover; border-radius: 4px; border: 1px solid #e2e8f0; }
    .footer { margin-top: 16px; color: #64748b; font-size: .9rem; }
    @media (prefers-color-scheme: dark) {
      thead th { background: #0b1220; }
      table, th, td, img { border-color: #1f2937; }
      tbody tr:hover { background: #0f172a; }
    }
  </style>
</head>
<body>
  <h1>{heading}</h1>
  <p class="meta">Source file: <code>{source}</code> • Items: <b>{count}</b></p>
  <table>
    <thead>
      <tr>
        <th>Cover</th>
        <th>Title</th>
        <th>Rating</th>
        <th>Price</th>
        <th>Availability</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>
  <p class="footer">Generated from Books to Scrape category page.</p>
</body>
</html>
"""

ROW_TEMPLATE = """
<tr>
  <td class="img"><img src="{image}" alt="{title}" loading="lazy" /></td>
  <td>{title}</td>
  <td><span class="rating">{rating}</span></td>
  <td class="price">{price}</td>
  <td>{stock_html}</td>
</tr>
"""


def absolutize_image(src: str) -> str:
    if src.startswith('http://') or src.startswith('https://'):
        return src
    # normalize typical relative path used by books.toscrape.com
    src = src.replace('../../../../media/', '')
    return urljoin(BASE_MEDIA, src)


def parse_cards(html: str):
    sel = Selector(text=html)
    cards = sel.css('.product_pod')
    items = []
    for c in cards:
        title = c.css('h3 > a::attr(title), h3 > a::text').get(default='').strip()
        rating = c.css('.star-rating').attrib.get('class', '').split()
        rating = rating[1] if len(rating) > 1 else ''
        img = c.css('.image_container img::attr(src)').get(default='').strip()
        image = absolutize_image(img)
        price = c.css('.price_color::text').get(default='').strip()
        in_stock = bool(c.css('.availability .icon-ok')) or 'In stock' in c.css('.availability::text').get(default='')
        items.append({
            'title': title,
            'rating': rating,
            'image': image,
            'price': price,
            'in_stock': in_stock,
        })
    return items


def render_table(items, source_name: str, heading: str):
    rows_html = []
    for it in items:
        stock_html = f"<span class='instock'>In stock</span>" if it['in_stock'] else f"<span class='outstock'>Out of stock</span>"
        rows_html.append(ROW_TEMPLATE.format(
            image=it['image'],
            title=(it['title'] or '').replace('"', '&quot;'),
            rating=it['rating'] or 'N/A',
            price=it['price'] or 'N/A',
            stock_html=stock_html,
        ))
    return HTML_TEMPLATE.format(
        title=heading,
        heading=heading,
        source=source_name,
        count=len(items),
        rows='\n'.join(rows_html)
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: python format_books_table.py <input_html> [output_html]")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    if not in_path.exists():
        print(f"Input file not found: {in_path}")
        sys.exit(1)

    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else in_path.with_name(in_path.stem + "_table.html")

    html = in_path.read_text(encoding='utf-8', errors='ignore')
    items = parse_cards(html)
    # Create heading from filename if possible
    heading = f"Books Table – {in_path.stem}"
    page = render_table(items, in_path.name, heading)
    out_path.write_text(page, encoding='utf-8')
    print(f"Wrote {len(items)} items to {out_path}")


if __name__ == '__main__':
    main()

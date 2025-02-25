
import requests
import json
from database.db_handler import insert_product

def scrape_shopify_store(store_url):
    """Scrape product data from a Shopify store."""
    api_url = f"{store_url.rstrip('/')}/products.json"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise error if request fails
        data = response.json()
        
        products = data.get("products", [])
        for product in products:
            product_data = {
                "name": product["title"],
                "desc": product.get("body_html", ""),
                "category": product.get("product_type", ""),
                "niche": "",  # Shopify doesn’t provide niche directly
                "images": [img["src"] for img in product.get("images", [])],
                "price": float(product["variants"][0]["price"]),
                "stock_status": product["variants"][0]["available"],
                "rating": None,  # Shopify JSON API doesn't include ratings
                "reviews": None,  # Shopify JSON API doesn't include reviews
                "seller": store_url
            }
            
            insert_product(product_data)

        print(f"✅ Scraped {len(products)} products from {store_url}")
    
    except Exception as e:
        print(f"❌ Failed to scrape {store_url}: {e}")


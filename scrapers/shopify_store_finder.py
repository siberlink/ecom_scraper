## MAIN SCRIPT ###
## Find Shopify Store -- Retrieve Location -- Save to DB

import sys
import os
# Ensure Python can find project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from utils.search_handler import find_shopify_stores
from utils.url_handler import extract_base_url
from utils.location_finder import get_store_location
from database.store_db_handler import save_shopify_stores_to_db

# Load environment variables
load_dotenv()

# 🔹 Global Variables (Modify These)
niche = "Gut Health Supplements"  # Change niche dynamically
max_results = 100  # Change number of stores to fetch

if __name__ == "__main__":
    print("🚀 [Shopify Store Finder] Finding Shopify stores...")
    stores = find_shopify_stores(niche, max_results)

    if stores:
        formatted_stores = []

        for store_data in stores:
            # ✅ Ensure unpacking correctly
            if isinstance(store_data, tuple) and len(store_data) == 3:
                final_url, country, city = store_data
            else:
                #print(f"⚠️ [Shopify Store Finder] Invalid store data format: {store_data}, skipping...")
                continue

            base_url, _ = extract_base_url(final_url)  # ✅ Ensure proper URL extraction

            if not base_url or not base_url.startswith("http"):
                #print(f"⚠️ [Shopify Store Finder] Invalid base URL extracted: {base_url}, skipping...")
                continue

            store_name = base_url.split("//")[-1].split(".")[0]  # Extract store name
            formatted_stores.append((base_url, store_name, niche, country, city))

            print(f"✅ [Shopify Store Finder] Found: {base_url} | {store_name} | {country}, {city}")

        if formatted_stores:
            save_shopify_stores_to_db(formatted_stores)
            print("✅ [Shopify Store Finder] Stores saved successfully!")
        else:
            print("❌ [Shopify Store Finder] No valid stores to save.")
    else:
        print("❌ [Shopify Store Finder] No Shopify stores found.")

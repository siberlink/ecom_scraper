## FIND SHOPIFY STORES
## correctly handle custom domains

import os
import time
from serpapi import GoogleSearch
from dotenv import load_dotenv
from utils.url_handler import extract_base_url
from utils.location_finder import get_store_location

# Load environment variables
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def find_shopify_stores(niche, max_results=100):
    """Find Shopify stores using Google Search API (SerpAPI) with pagination & robust error handling."""
    found_stores = []
    results_per_page = 20  # Adjust for efficiency (20 is a safe limit)

    try:
        for start in range(0, max_results, results_per_page):

            params = {
                "q": f"site:.myshopify.com {niche} -inurl:collections -inurl:products -inurl:cart -inurl:account -inurl:checkout -inurl:search -inurl:blog -inurl:pages -inurl:help",
                "num": results_per_page,
                "start": start,  # Pagination
                "api_key": SERPAPI_KEY,
                "google_domain": "google.com",  # Use google.com for USA (change if needed)
                "gl": "us",  # Restrict results to U.S.
                "hl": "en",  # Language: English
                "filter": 0,  # Include omitted results
            }

            print(f"🔍 [Search Handler] Fetching results {start+1}-{start+results_per_page} for {niche}...")

            try:
                search = GoogleSearch(params)
                results = search.get_dict()

                if results is None:
                    print("⚠️ [Search Handler] Received empty response from SerpAPI! Skipping this batch...")
                    continue  # Skip this batch and continue

                if not results.get("organic_results"):
                    print("⚠️ [Search Handler] No `organic_results` found! Possible rate limit or Google block.")
                    break  # Stop fetching if no results

            except Exception as e:
                print(f"❌ [Search Handler] Failed to fetch search results: {e}")
                continue  # Skip to next request

            for result in results.get("organic_results", []):
                try:
                    store_url = result.get("link")
                    if not store_url:
                        print(f"⚠️ [Search Handler] Skipping malformed result: {result}")
                        continue

                    extracted = extract_base_url(store_url)
                    if not extracted or extracted[0] is None:
                        print(f"⚠️ [Search Handler] Failed to extract base URL from {store_url}, skipping...")
                        continue

                    clean_url, custom_domain = extracted
                    final_url = custom_domain if custom_domain else clean_url  # Use custom domain if available

                    if final_url.startswith("http"):
                        print(f"🔗 [Search Handler] Found Store: {final_url}")

                        # 🔍 Fetch store location
                        location = get_store_location(final_url)
                        country = location.get("country", "Unknown")
                        city = location.get("city", "Unknown")

                        found_stores.append((final_url, country, city))

                except Exception as e:
                    print(f"⚠️ [Search Handler] Error processing result {result}: {e}")
                    continue  # Skip this result and continue

            print(f"✅ [Search Handler] Total Stores Found So Far: {len(found_stores)}")
            
            # ✅ Delay between requests to avoid hitting API limits
            time.sleep(5)  # Wait 5 seconds before next request

    except Exception as e:
        print(f"❌ [Search Handler] Unexpected error: {e}")

    return found_stores  # ✅ Return the final list of stores found

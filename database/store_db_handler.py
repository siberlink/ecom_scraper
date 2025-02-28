## properly handle the extracted store names.

import psycopg2
from config.settings import DB_CONFIG

def save_shopify_stores_to_db(stores):
    """Save found Shopify stores into the database."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                for store in stores:
                    try:
                        # ✅ Ensure tuple has exactly 5 values before unpacking
                        if len(store) != 5:
                            #print(f"⚠️ [Store DB Handler] Skipping invalid store data: {store}")
                            continue

                        store_url, store_name, niche, country, city = store

                        cur.execute(
                            """INSERT INTO shopify_stores (store_url, store_name, niche, country, city, last_scraped, created_at) 
                               VALUES (%s, %s, %s, %s, %s, NOW(), NOW()) 
                               ON CONFLICT (store_url) DO UPDATE 
                               SET last_scraped = NOW(), country = EXCLUDED.country, city = EXCLUDED.city""",
                            (store_url, store_name, niche, country, city),
                        )
                        #print(f"✅ Saved to DB: {store_url} | {store_name} | {niche} | {country}, {city}")

                    except Exception as e:
                        print(f"❌ [Store DB Handler] Failed to save {store_url}: {e}")

            conn.commit()
        #print("✅ [Store DB Handler] Stores saved successfully!")

    except Exception as e:
        print(f"❌ [Store DB Handler] Database connection failed: {e}")

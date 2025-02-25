
import psycopg2
from config.settings import DB_CONFIG

def connect_db():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def insert_product(data):
    """Insert a product into the database."""
    conn = connect_db()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO products (p_name, p_desc, p_categ, p_niche, p_images, 
                                  p_price, p_stock_status, p_rating, p_reviews, 
                                  p_seller, p_scraped_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """,
            (
                data["name"], data["desc"], data["category"], data["niche"], data["images"],
                data["price"], data["stock_status"], data["rating"], data["reviews"], data["seller"]
            )
        )
        conn.commit()
        cur.close()
        print("✅ Product inserted successfully!")
    except Exception as e:
        print(f"❌ Failed to insert product: {e}")
    finally:
        conn.close()

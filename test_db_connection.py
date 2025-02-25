import psycopg2

# Database configuration
DB_CONFIG = {
    "dbname": "ecom_scraped",
    "user": "postgres",
    "password": "Esaas@2267",
    "host": "localhost",
    "port": "5432",
}

# Test connection
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("✅ Database connection successful!")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")

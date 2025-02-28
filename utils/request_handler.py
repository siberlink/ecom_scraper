
import requests

def fetch_shopify_json(url):
    """Fetch Shopify JSON data."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ [Request Handler] Request failed: {e}")
        return None

## Fixing Store Name Extraction
## ensures both Shopify subdomains and custom domains are handled correctly

import requests
from urllib.parse import urlparse

def extract_base_url(store_url):
    """Extracts the base domain from a Shopify store URL and detects if it redirects to a custom domain."""
    try:
        response = requests.get(store_url, allow_redirects=True, timeout=10)
        final_url = response.url  # Get the final redirected URL

        parsed_url = urlparse(final_url)
        domain = parsed_url.netloc  # Extracts domain name without protocol (e.g., "example.com")

        # ✅ Ensure custom domains return a properly formatted URL
        if "myshopify.com" not in domain:
            custom_domain = f"https://{domain}"
            #print(f"🔄 [URL Handler] Redirect Detected → Custom Domain: {custom_domain}")
            return custom_domain, final_url  # ✅ Always returns full URL

        # If still on Shopify, return original URL
        return store_url, None

    except requests.RequestException as e:
        print(f"❌ [URL Handler] Error extracting base URL from {store_url}: {e}")
        return None, None  # Ensure consistent return format

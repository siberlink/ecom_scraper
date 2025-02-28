## Find The Location of the Store

import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 🌎 Global Default Country Setting
DEFAULT_COUNTRY = "US"

def fetch_page_content(url):
    """Fetch page HTML content safely."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"⚠️ [Location Finder] Failed to fetch {url} (Status: {response.status_code})")
            return None
        
        return BeautifulSoup(response.text, "html.parser")

    except requests.RequestException as e:
        print(f"❌ [Location Finder] Error fetching {url}: {e}")
        return None

def extract_location_from_text(text):
    """Extract city and country from raw text using regex."""
    if not text:  # ✅ Check if text is None or empty
        return {"country": DEFAULT_COUNTRY, "city": "Unknown"}

    try:
        address_patterns = [
            r"([A-Z][a-z]+,\s?[A-Z]{2})",  # Example: New York, NY
            r"([A-Z][a-z]+\s?[A-Z][a-z]+,?\s?[A-Z]{2})",  # Example: Los Angeles, CA
            r"(\d{1,5}\s\w+.*?,\s?[A-Z][a-z]+\s?,?\s?[A-Z]{2}\s?\d{5})",  # Example: 123 Main St, New York, NY 10001
        ]

        for pattern in address_patterns:
            match = re.search(pattern, text)
            if match:
                location = match.group(0)
                city, country = location.split(",")[:2] if "," in location else ("Unknown", DEFAULT_COUNTRY)
                return {"country": country.strip(), "city": city.strip()}
    except Exception as e:
        print(f"⚠️ [Location Finder] Regex error: {e}")

    return {"country": DEFAULT_COUNTRY, "city": "Unknown"}  # ✅ Uses DEFAULT_COUNTRY

def extract_location_from_schema(soup):
    """Extract location from Schema.org structured data."""
    if not soup:  # ✅ Ensure soup is not None before parsing
        return {"country": DEFAULT_COUNTRY, "city": "Unknown"}

    try:
        for script in soup.find_all("script", type="application/ld+json"):
            if not script.string:
                continue  # Skip empty JSON data
            
            try:
                data = json.loads(script.string)
            except json.JSONDecodeError as e:
                print(f"⚠️ [Location Finder] JSON Decode Error: {e}")
                continue  # ✅ Continue to the next script instead of failing

            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "address" in item:
                        address = item["address"]
                        country = address.get("addressCountry", DEFAULT_COUNTRY)
                        city = address.get("addressLocality", "Unknown")
                        return {"country": country, "city": city}
            elif isinstance(data, dict) and "address" in data:
                address = data["address"]
                country = address.get("addressCountry", DEFAULT_COUNTRY)
                city = address.get("addressLocality", "Unknown")
                return {"country": country, "city": city}

    except Exception as e:
        print(f"⚠️ [Location Finder] Unexpected error while parsing schema: {e}")

    return {"country": DEFAULT_COUNTRY, "city": "Unknown"}  # ✅ Uses DEFAULT_COUNTRY

def get_store_location(store_url):
    """Finds store location from Contact Us, About Us, Footer, or Schema.org."""
    print(f"🔍 [Location Finder] Checking store: {store_url}")

    # Fetch Main Page
    soup = fetch_page_content(store_url)
    if not soup:
        print(f"⚠️ [Location Finder] Skipping {store_url} (No content retrieved)")
        return {"country": DEFAULT_COUNTRY, "city": "Unknown"}

    # Check Schema.org Data
    location = extract_location_from_schema(soup)
    if location["country"] != DEFAULT_COUNTRY:
        print(f"✅ [Location Finder] Found Schema.org Location: {location}")
        return location

    # Look for Contact Page
    contact_page = None
    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        if "contact" in link.get_text(strip=True).lower():
            contact_page = urljoin(store_url, href)
            break

    if contact_page:
        print(f"🔎 [Location Finder] Checking Contact Page: {contact_page}")
        soup = fetch_page_content(contact_page)
        if soup:
            text_content = soup.get_text(" ", strip=True) if soup else ""
            location = extract_location_from_text(text_content)
            if location["country"] != DEFAULT_COUNTRY:
                return location

    # If still unknown, check Footer & About Us Page
    footer_text = soup.find("footer").get_text(" ", strip=True) if soup.find("footer") else ""
    if footer_text:  # ✅ Ensure footer_text is not None
        location = extract_location_from_text(footer_text)
        if location["country"] != DEFAULT_COUNTRY:
            return location

    # Look for About Page
    about_page = None
    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        if "about" in link.get_text(strip=True).lower():
            about_page = urljoin(store_url, href)
            break

    if about_page:
        print(f"🔎 [Location Finder] Checking About Page: {about_page}")
        soup = fetch_page_content(about_page)
        if soup:
            text_content = soup.get_text(" ", strip=True) if soup else ""
            location = extract_location_from_text(text_content)
            if location["country"] != DEFAULT_COUNTRY:
                return location

    print(f"⚠️ [Location Finder] No location found for {store_url}")
    return {"country": DEFAULT_COUNTRY, "city": "Unknown"}  # ✅ Uses DEFAULT_COUNTRY

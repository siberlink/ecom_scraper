
import requests

GEOLOCATION_API_URL = "https://api.ipgeolocation.io/ipgeo"
GEOLOCATION_API_KEY = "dcab0e7209d84b45ac4f2d0394ed55dc"

test_ip = "8.8.8.8"  # Google's public IP
response = requests.get(f"{GEOLOCATION_API_URL}?apiKey={GEOLOCATION_API_KEY}&ip={test_ip}")
print(response.json())  # Should return location data

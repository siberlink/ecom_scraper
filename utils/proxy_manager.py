
import os
from config.brightdata import BRIGHTDATA_PROXY

def get_brightdata_proxy():
    """Generate a BrightData proxy dictionary."""
    return {
        "http": f"http://{BRIGHTDATA_PROXY['username']}:{BRIGHTDATA_PROXY['password']}@{BRIGHTDATA_PROXY['host']}:{BRIGHTDATA_PROXY['port']}",
        "https": f"http://{BRIGHTDATA_PROXY['username']}:{BRIGHTDATA_PROXY['password']}@{BRIGHTDATA_PROXY['host']}:{BRIGHTDATA_PROXY['port']}",
    }


import requests
from django.conf import settings

RAWG_API_KEY = settings.RAWG_API_KEY

BASE = getattr(settings, "RAWG_APT_BASE", "https://api.rawg.io/api")
KEY = getattr(settings, "RAWG_API_KEY", "")

def rawg_search(query, page_size=40, max_results=100):
    results = []
    page = 1
    while len(results) < max_results:
        url = f"{BASE}/games"
        params = {
            "key": RAWG_API_KEY,
            "search": query,
            "page": page,
            "page_size": min(page_size, max_results - len(results)),
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json().get("results", [])

            if not data:
                break # no more results

            results.extend(data)

            if len(data) < params["page_size"]:
                break # last page reached

            page += 1

        except Exception as e:
            print("RAWG API search error:", e)
            break

    # Only return the list of games
    return results

def rawg_game_detail(rawg_id):
    url = f"{BASE}/games/{rawg_id}"
    params = {}
    if KEY:
        params["key"] = KEY
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()
"""Small, dependency-free InstNews REST client (Python 3.10+)."""
import json
import os
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class InstNews:
    """Pass api_key (an InstNews dashboard key, sent as X-API-Key) to use a
    Pro/Max tier; leave it unset for the anonymous free tier."""

    def __init__(self, api_key=None, base_url="https://www.instnews.net", timeout=20):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get(self, path, params=None):
        query = urlencode({k: v for k, v in (params or {}).items() if v is not None})
        url = self.base_url + path + ("?" + query if query else "")
        headers = {"Accept": "application/json", "User-Agent": "instnews-python-example/0.1"}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        try:
            with urlopen(Request(url, headers=headers), timeout=self.timeout) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code == 429:
                retry = error.headers.get("Retry-After", "unspecified")
                raise RuntimeError(f"Rate limited; Retry-After: {retry}") from error
            raise

    def news(self, limit=10, **filters):
        return self._get("/api/news", {"limit": limit, **filters})

    def sources(self):
        return self._get("/api/sources")

    def stats(self):
        return self._get("/api/stats")


if __name__ == "__main__":
    client = InstNews(api_key=os.environ.get("INSTNEWS_API_KEY"))
    print(json.dumps(client.news(limit=1), indent=2))

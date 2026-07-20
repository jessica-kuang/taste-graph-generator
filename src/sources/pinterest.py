import time
from pathlib import Path
from urllib.parse import urlencode

import requests

import config
from sources.base import ImageSource

AUTHORIZE_URL = "https://www.pinterest.com/oauth/"
TOKEN_URL = "https://api.pinterest.com/v5/oauth/token"
API_BASE = "https://api.pinterest.com/v5"
SCOPES = "boards:read,pins:read"


class PinterestSource(ImageSource):
    name = "pinterest"

    def is_connected(self) -> bool:
        return config.load_token(self.name) is not None

    def connect_url(self) -> str | None:
        params = {
            "client_id": config.require("PINTEREST_CLIENT_ID"),
            "redirect_uri": config.require("PINTEREST_REDIRECT_URI"),
            "response_type": "code",
            "scope": SCOPES,
        }
        return f"{AUTHORIZE_URL}?{urlencode(params)}"

    def handle_callback(self, code: str) -> None:
        response = requests.post(
            TOKEN_URL,
            auth=(config.require("PINTEREST_CLIENT_ID"), config.require("PINTEREST_CLIENT_SECRET")),
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": config.require("PINTEREST_REDIRECT_URI"),
            },
        )
        response.raise_for_status()
        token = response.json()
        token["obtained_at"] = time.time()
        config.save_token(self.name, token)

    def _refresh(self, token: dict) -> dict:
        response = requests.post(
            TOKEN_URL,
            auth=(config.require("PINTEREST_CLIENT_ID"), config.require("PINTEREST_CLIENT_SECRET")),
            data={"grant_type": "refresh_token", "refresh_token": token["refresh_token"]},
        )
        response.raise_for_status()
        refreshed = response.json()
        refreshed["obtained_at"] = time.time()
        refreshed.setdefault("refresh_token", token["refresh_token"])
        config.save_token(self.name, refreshed)
        return refreshed

    def _get(self, path: str, token: dict, params: dict | None = None) -> dict:
        headers = {"Authorization": f"Bearer {token['access_token']}"}
        response = requests.get(f"{API_BASE}{path}", headers=headers, params=params)
        if response.status_code == 401:
            token = self._refresh(token)
            headers = {"Authorization": f"Bearer {token['access_token']}"}
            response = requests.get(f"{API_BASE}{path}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_images(self, dest_dir: Path, limit: int = 50) -> list[Path]:
        token = config.load_token(self.name)
        if token is None:
            raise RuntimeError("Pinterest is not connected yet, visit /auth/pinterest/start first")

        dest_dir.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []

        boards = self._get("/boards", token, params={"page_size": 25}).get("items", [])
        for board in boards:
            if len(written) >= limit:
                break
            pins = self._get(f"/boards/{board['id']}/pins", token, params={"page_size": 25}).get("items", [])
            for pin in pins:
                if len(written) >= limit:
                    break
                images = pin.get("media", {}).get("images", {})
                best = images.get("orig") or next(iter(images.values()), None)
                if not best:
                    continue
                image_response = requests.get(best["url"])
                if image_response.status_code != 200:
                    continue
                suffix = Path(best["url"]).suffix.split("?")[0] or ".jpg"
                dest = dest_dir / f"pinterest_{pin['id']}{suffix}"
                dest.write_bytes(image_response.content)
                written.append(dest)

        return written


if __name__ == "__main__":
    source = PinterestSource()
    if not source.is_connected():
        print(f"not connected, visit this URL to authorize: {source.connect_url()}")
    else:
        written = source.fetch_images(config.UPLOADS_DIR, limit=50)
        print(f"downloaded {len(written)} pins to {config.UPLOADS_DIR}")

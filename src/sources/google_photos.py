import time
import webbrowser
from pathlib import Path
from urllib.parse import urlencode

import requests

import config
from sources.base import ImageSource

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
PICKER_API_BASE = "https://photospicker.googleapis.com/v1"
SCOPE = "https://www.googleapis.com/auth/photospicker.mediaitems.readonly"


class GooglePhotosSource(ImageSource):
    """Google restricted broad Photos library scanning for non-verified apps
    around March 2025. The realistic pattern now is the Picker API: create a
    session, the user picks specific photos in a Google-hosted UI, then the
    app polls the session and downloads only what was picked. This is not
    "connect once, sync forever" like Pinterest, every fetch is a fresh pick.
    """

    name = "google_photos"

    def is_connected(self) -> bool:
        return config.load_token(self.name) is not None

    def connect_url(self) -> str | None:
        params = {
            "client_id": config.require("GOOGLE_CLIENT_ID"),
            "redirect_uri": config.require("GOOGLE_REDIRECT_URI"),
            "response_type": "code",
            "scope": SCOPE,
            "access_type": "offline",
            "prompt": "consent",
        }
        return f"{AUTHORIZE_URL}?{urlencode(params)}"

    def handle_callback(self, code: str) -> None:
        response = requests.post(
            TOKEN_URL,
            data={
                "client_id": config.require("GOOGLE_CLIENT_ID"),
                "client_secret": config.require("GOOGLE_CLIENT_SECRET"),
                "code": code,
                "redirect_uri": config.require("GOOGLE_REDIRECT_URI"),
                "grant_type": "authorization_code",
            },
        )
        response.raise_for_status()
        token = response.json()
        token["obtained_at"] = time.time()
        config.save_token(self.name, token)

    def _refresh(self, token: dict) -> dict:
        response = requests.post(
            TOKEN_URL,
            data={
                "client_id": config.require("GOOGLE_CLIENT_ID"),
                "client_secret": config.require("GOOGLE_CLIENT_SECRET"),
                "refresh_token": token["refresh_token"],
                "grant_type": "refresh_token",
            },
        )
        response.raise_for_status()
        refreshed = response.json()
        refreshed["obtained_at"] = time.time()
        refreshed.setdefault("refresh_token", token["refresh_token"])
        config.save_token(self.name, refreshed)
        return refreshed

    def _headers(self, token: dict) -> dict:
        return {"Authorization": f"Bearer {token['access_token']}"}

    def _authed_request(self, method: str, url: str, **kwargs) -> requests.Response:
        token = config.load_token(self.name)
        if token is None:
            raise RuntimeError("Google Photos is not connected yet, visit /auth/google/start first")
        response = requests.request(method, url, headers=self._headers(token), **kwargs)
        if response.status_code == 401:
            token = self._refresh(token)
            response = requests.request(method, url, headers=self._headers(token), **kwargs)
        response.raise_for_status()
        return response

    def create_picker_session(self) -> dict:
        return self._authed_request("POST", f"{PICKER_API_BASE}/sessions").json()

    def poll_session(self, session_id: str) -> dict:
        return self._authed_request("GET", f"{PICKER_API_BASE}/sessions/{session_id}").json()

    def list_media_items(self, session_id: str) -> list[dict]:
        items = []
        page_token = None
        while True:
            params = {"sessionId": session_id}
            if page_token:
                params["pageToken"] = page_token
            data = self._authed_request("GET", f"{PICKER_API_BASE}/mediaItems", params=params).json()
            items.extend(data.get("mediaItems", []))
            page_token = data.get("nextPageToken")
            if not page_token:
                break
        return items

    def download_media_items(self, items: list[dict], dest_dir: Path, limit: int = 50) -> list[Path]:
        token = config.load_token(self.name)
        dest_dir.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for item in items[:limit]:
            media_file = item.get("mediaFile", {})
            base_url = media_file.get("baseUrl")
            if not base_url:
                continue
            response = requests.get(f"{base_url}=d", headers=self._headers(token))
            if response.status_code != 200:
                continue
            suffix = Path(media_file.get("filename", "")).suffix or ".jpg"
            dest = dest_dir / f"googlephotos_{item['id']}{suffix}"
            dest.write_bytes(response.content)
            written.append(dest)
        return written

    def fetch_images(self, dest_dir: Path, limit: int = 50, timeout_seconds: int = 300) -> list[Path]:
        """Blocking convenience path for CLI use: opens the picker in a
        browser and polls until the user finishes selecting or timeout_seconds
        elapses. The web UI (routes.py) drives this in two steps instead so
        the HTTP request doesn't block on a person picking photos.
        """
        session = self.create_picker_session()
        print(f"opening picker: {session['pickerUri']}")
        webbrowser.open(session["pickerUri"])

        poll_interval = float(session.get("pollingConfig", {}).get("pollInterval", "5s").rstrip("s"))
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            session = self.poll_session(session["id"])
            if session.get("mediaItemsSet"):
                break
            time.sleep(poll_interval)
        else:
            raise TimeoutError("timed out waiting for photos to be picked")

        items = self.list_media_items(session["id"])
        return self.download_media_items(items, dest_dir, limit=limit)


if __name__ == "__main__":
    source = GooglePhotosSource()
    if not source.is_connected():
        print(f"not connected, visit this URL to authorize: {source.connect_url()}")
    else:
        written = source.fetch_images(config.UPLOADS_DIR, limit=50)
        print(f"downloaded {len(written)} picked photos to {config.UPLOADS_DIR}")

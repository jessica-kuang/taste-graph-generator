import json
import time
from collections import Counter
from urllib.parse import urlencode

import anthropic
import requests

import config

AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE = "https://api.spotify.com/v1"
SCOPE = "user-top-read"


class SpotifySource:
    """Not an ImageSource, this feeds schema.py's existing (currently unused)
    MusicMood field rather than data/uploads/. Kept as its own narrow
    interface instead of forcing it into the image-source ABC.
    """

    name = "spotify"

    def is_connected(self) -> bool:
        return config.load_token(self.name) is not None

    def connect_url(self) -> str:
        params = {
            "client_id": config.require("SPOTIFY_CLIENT_ID"),
            "response_type": "code",
            "redirect_uri": config.require("SPOTIFY_REDIRECT_URI"),
            "scope": SCOPE,
        }
        return f"{AUTHORIZE_URL}?{urlencode(params)}"

    def handle_callback(self, code: str) -> None:
        response = requests.post(
            TOKEN_URL,
            auth=(config.require("SPOTIFY_CLIENT_ID"), config.require("SPOTIFY_CLIENT_SECRET")),
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": config.require("SPOTIFY_REDIRECT_URI"),
            },
        )
        response.raise_for_status()
        token = response.json()
        token["obtained_at"] = time.time()
        config.save_token(self.name, token)

    def _refresh(self, token: dict) -> dict:
        response = requests.post(
            TOKEN_URL,
            auth=(config.require("SPOTIFY_CLIENT_ID"), config.require("SPOTIFY_CLIENT_SECRET")),
            data={"grant_type": "refresh_token", "refresh_token": token["refresh_token"]},
        )
        response.raise_for_status()
        refreshed = response.json()
        refreshed["obtained_at"] = time.time()
        refreshed.setdefault("refresh_token", token["refresh_token"])
        config.save_token(self.name, refreshed)
        return refreshed

    def _get_top_artists(self) -> list[dict]:
        token = config.load_token(self.name)
        if token is None:
            raise RuntimeError("Spotify is not connected yet, visit /auth/spotify/start first")

        headers = {"Authorization": f"Bearer {token['access_token']}"}
        response = requests.get(
            f"{API_BASE}/me/top/artists", headers=headers, params={"time_range": "medium_term", "limit": 20}
        )
        if response.status_code == 401:
            token = self._refresh(token)
            headers = {"Authorization": f"Bearer {token['access_token']}"}
            response = requests.get(
                f"{API_BASE}/me/top/artists", headers=headers, params={"time_range": "medium_term", "limit": 20}
            )
        response.raise_for_status()
        return response.json().get("items", [])

    def _describe_taste(self, client: anthropic.Anthropic, genres: list[str] = None, artists: list[str] = None) -> list[str]:
        if genres:
            signal = f"Someone's top Spotify genres are: {', '.join(genres)}."
        else:
            # Spotify's API has stopped returning genre tags for most artists,
            # so fall back to inferring mood from the artist names themselves,
            # the same "Claude names the raw signal" pattern palette.py already
            # uses for k-means colors.
            signal = f"Someone's top Spotify artists are: {', '.join(artists)}."

        message = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": f"""{signal}

Turn this into 3-5 evocative one-or-two-word mood descriptors for their
listening taste (e.g. "melancholic", "cinematic", "sun-warmed"). Never
generic. Respond with ONLY a comma-separated list, nothing else."""
            }]
        )
        return [d.strip() for d in message.content[0].text.split(",") if d.strip()]

    def fetch_taste_signals(self) -> dict:
        artists = self._get_top_artists()
        genre_counts = Counter(genre for artist in artists for genre in artist.get("genres") or [])
        top_genres = [genre for genre, _ in genre_counts.most_common(10)]
        reference_artists = [artist["name"] for artist in artists[:5]]

        descriptors = []
        if top_genres:
            descriptors = self._describe_taste(anthropic.Anthropic(), genres=top_genres)
        elif reference_artists:
            descriptors = self._describe_taste(anthropic.Anthropic(), artists=reference_artists)

        music_mood = {"descriptors": descriptors, "reference_artists": reference_artists}
        config.PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        (config.PROFILES_DIR / "music_mood.json").write_text(json.dumps(music_mood, indent=2))
        return music_mood

    def status(self) -> dict:
        return {"name": self.name, "connected": self.is_connected()}


if __name__ == "__main__":
    source = SpotifySource()
    if not source.is_connected():
        print(f"not connected, visit this URL to authorize: {source.connect_url()}")
    else:
        music_mood = source.fetch_taste_signals()
        print(f"wrote music_mood.json: {music_mood}")

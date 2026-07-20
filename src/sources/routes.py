from flask import Blueprint, jsonify, redirect, render_template, request, url_for

import config
from pipeline import PipelineError, run_pipeline
from sources.apple_photos import ApplePhotosSource
from sources.google_photos import GooglePhotosSource
from sources.pinterest import PinterestSource
from sources.spotify import SpotifySource

bp = Blueprint("sources", __name__)

IMAGE_SOURCES = {
    "apple_photos": ApplePhotosSource(),
    "pinterest": PinterestSource(),
    "google_photos": GooglePhotosSource(),
}
SPOTIFY = SpotifySource()

OAUTH_PROVIDERS = {
    "pinterest": IMAGE_SOURCES["pinterest"],
    "google_photos": IMAGE_SOURCES["google_photos"],
    "spotify": SPOTIFY,
}


@bp.route("/connect")
def connect():
    return render_template("connect.html")


@bp.route("/auth/<provider>/start")
def auth_start(provider):
    source = OAUTH_PROVIDERS.get(provider)
    if source is None:
        return jsonify({"error": f"unknown provider {provider}"}), 404
    return redirect(source.connect_url())


@bp.route("/auth/<provider>/callback")
def auth_callback(provider):
    source = OAUTH_PROVIDERS.get(provider)
    if source is None:
        return jsonify({"error": f"unknown provider {provider}"}), 404
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "missing code"}), 400
    source.handle_callback(code)
    return redirect(url_for("sources.connect"))


@bp.route("/api/sources/status")
def sources_status():
    status = {name: source.status() for name, source in IMAGE_SOURCES.items()}
    status["spotify"] = SPOTIFY.status()
    return jsonify(status)


@bp.route("/api/sources/<provider>/fetch", methods=["POST"])
def sources_fetch(provider):
    if provider == "spotify":
        try:
            music_mood = SPOTIFY.fetch_taste_signals()
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        return jsonify({"ok": True, "music_mood": music_mood})

    source = IMAGE_SOURCES.get(provider)
    if source is None:
        return jsonify({"error": f"unknown provider {provider}"}), 404
    try:
        written = source.fetch_images(config.UPLOADS_DIR, limit=50)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ok": True, "count": len(written)})


@bp.route("/api/generate", methods=["POST"])
def generate():
    try:
        run_pipeline()
    except PipelineError as e:
        return jsonify({"error": str(e), "stage": e.stage}), 500
    return jsonify({"ok": True})

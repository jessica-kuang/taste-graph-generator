from pathlib import Path

from sources.base import ImageSource

SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def _convert_if_unsupported(path: Path) -> Path:
    """embedder.py only recognizes jpg/jpeg/png/webp, but Photos.app exports
    HEIC by default on modern iPhones. Convert anything else to JPEG here so
    embedder.py never needs to know about Apple's format, keeping it untouched.
    """
    if path.suffix.lower() in SUPPORTED_SUFFIXES:
        return path

    import pillow_heif
    from PIL import Image

    pillow_heif.register_heif_opener()
    converted = path.with_suffix(".jpg")
    Image.open(path).convert("RGB").save(converted, "JPEG")
    path.unlink()
    return converted


class ApplePhotosSource(ImageSource):
    """Reads the local Photos.app library directly via osxphotos.

    No OAuth, no developer account, no cloud round trip: the only gate is
    macOS's native Photos permission prompt, which fires the first time the
    process calling this reads the library. Pulls favorited photos as the
    proxy for "images that feel like you" since that's the closest existing
    signal to a mood board without asking the user to curate anything new.
    """

    name = "apple_photos"

    def is_connected(self) -> bool:
        try:
            import osxphotos

            osxphotos.PhotosDB()
            return True
        except Exception:
            return False

    def fetch_images(self, dest_dir: Path, limit: int = 50) -> list[Path]:
        import osxphotos

        db = osxphotos.PhotosDB()
        favorites = [
            photo for photo in db.photos(images=True, movies=False)
            if photo.favorite and not photo.ismissing
        ]
        favorites.sort(key=lambda p: p.date, reverse=True)

        dest_dir.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for photo in favorites[:limit]:
            suffix = Path(photo.original_filename).suffix or ".jpg"
            filename = f"applephotos_{photo.uuid}{suffix}"
            try:
                exported = photo.export(str(dest_dir), filename=filename, overwrite=True)
            except Exception as e:
                print(f"skipping {photo.original_filename}: {e}")
                continue
            written.extend(_convert_if_unsupported(Path(p)) for p in exported)

        return written


if __name__ == "__main__":
    from config import UPLOADS_DIR

    source = ApplePhotosSource()
    print(f"connected: {source.is_connected()}")

    written = source.fetch_images(UPLOADS_DIR, limit=50)
    print(f"exported {len(written)} favorited photos to {UPLOADS_DIR}")

from abc import ABC, abstractmethod
from pathlib import Path


class ImageSource(ABC):
    """Common interface for anything that can populate data/uploads/ with images.

    embedder.py only globs data/uploads/ by file extension, it has no concept
    of where an image came from, so every source just needs to land files
    there. Nothing downstream of embedder.py needs to know a source exists.
    """

    name: str

    @abstractmethod
    def is_connected(self) -> bool:
        ...

    def connect_url(self) -> str | None:
        """OAuth authorize URL, or None for sources with no OAuth step (e.g. local Apple Photos)."""
        return None

    def handle_callback(self, code: str) -> None:
        """Exchange an OAuth code for tokens and persist them. No-op for non-OAuth sources."""
        raise NotImplementedError(f"{self.name} has no OAuth callback")

    @abstractmethod
    def fetch_images(self, dest_dir: Path, limit: int = 50) -> list[Path]:
        """Fetch images into dest_dir, returning the paths written."""
        ...

    def status(self) -> dict:
        return {"name": self.name, "connected": self.is_connected()}

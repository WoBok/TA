from __future__ import annotations
import os
import sys
from typing import Optional

class ResourceLoader:
    """Simple resource loader that resolves paths for dev and PyInstaller bundle.
    Extend with image/font/sound helpers as needed.
    """

    def __init__(self, base: Optional[str] = None) -> None:
        if base is not None:
            self.base_path = base
        else:
            try:
                self.base_path = sys._MEIPASS  # type: ignore[attr-defined]
            except Exception:
                self.base_path = os.path.abspath(".")

    def path(self, relative_path: str) -> str:
        return os.path.join(self.base_path, relative_path)


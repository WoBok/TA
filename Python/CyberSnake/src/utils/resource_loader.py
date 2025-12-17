import os
import sys

def resource_path(relative_path: str) -> str:
    """Resolve resource path for both dev and PyInstaller bundle.
    When bundled by PyInstaller, resources are in a temporary folder stored in sys._MEIPASS.
    """
    try:
        base_path = sys._MEIPASS  # type: ignore[attr-defined]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


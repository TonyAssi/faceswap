"""
Face Swap - Thin Client (HF Space backend)

Calls the Hugging Face Space:
    tonyassi/face-swap

Public API:
    swap_faces(src_img, dest_img)

Inputs:
    - str filepath
    - PIL.Image.Image
    - numpy array (H, W, 3/4)

Output:
    - PIL.Image.Image (RGB)

Notes:
    - Requires Python 3.10+
    - Uses handle_file() (no deprecated file() usage)
"""

from __future__ import annotations

import os
import sys
import tempfile
from typing import Union, Any, Optional

import numpy as np
from PIL import Image

from gradio_client import Client, handle_file


# ----------------------------
# Types
# ----------------------------
ImageLike = Union[str, np.ndarray, Image.Image]


# ----------------------------
# Config
# ----------------------------
SPACE_ID = os.getenv("FACE_SWAP_SPACE_ID", "tonyassi/face-swap")
API_NAME = os.getenv("FACE_SWAP_API_NAME", "/swap_faces")


# ----------------------------
# Errors
# ----------------------------
class FaceSwapClientError(Exception):
    pass


class InvalidImageError(FaceSwapClientError):
    pass


class RemoteInitError(FaceSwapClientError):
    pass


class RemoteCallError(FaceSwapClientError):
    pass


# ----------------------------
# Python version guard
# ----------------------------
def _require_py310():
    if sys.version_info < (3, 10):
        raise RemoteInitError(
            "Python 3.10+ is required for this Face Swap client."
        )


# ----------------------------
# Singleton client
# ----------------------------
_CLIENT: Optional[Client] = None


def _get_client() -> Client:
    global _CLIENT
    _require_py310()

    if _CLIENT is not None:
        return _CLIENT

    try:
        _CLIENT = Client(SPACE_ID, verbose=False)
        return _CLIENT
    except Exception as e:
        raise RemoteInitError(
            f"Failed to initialize Gradio Client for Space '{SPACE_ID}'."
        ) from e


# ----------------------------
# Image prep
# ----------------------------
def _to_temp_png_path(img: ImageLike) -> str:
    if img is None:
        raise InvalidImageError("Image is None.")

    # Path
    if isinstance(img, str):
        if not os.path.exists(img):
            raise InvalidImageError(f"File not found: {img}")
        return img

    # PIL
    if isinstance(img, Image.Image):
        pil = img.convert("RGB")
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.close()
        pil.save(tmp.name, format="PNG")
        return tmp.name

    # numpy
    if isinstance(img, np.ndarray):
        arr = img
        if arr.ndim != 3 or arr.shape[2] not in (3, 4):
            raise InvalidImageError("Numpy image must be HxWx3 or HxWx4.")

        if arr.dtype != np.uint8:
            arr = np.clip(arr, 0, 255).astype(np.uint8)

        if arr.shape[2] == 4:
            arr = arr[:, :, :3]

        pil = Image.fromarray(arr).convert("RGB")
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.close()
        pil.save(tmp.name, format="PNG")
        return tmp.name

    raise InvalidImageError(
        f"Unsupported image type: {type(img)}. Use str, PIL.Image, or numpy."
    )


def _cleanup_temp(path: str, original_input: ImageLike):
    try:
        if not isinstance(original_input, str) and path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def _normalize_result_to_pil(result: Any) -> Image.Image:
    # Your Space returns an Image dict-like object.
    # gradio_client usually converts it to:
    #   {"path": "...", ...}
    if isinstance(result, dict) and "path" in result and result["path"]:
        return Image.open(result["path"]).convert("RGB")

    if isinstance(result, str) and os.path.exists(result):
        return Image.open(result).convert("RGB")

    if isinstance(result, (list, tuple)) and result:
        return _normalize_result_to_pil(result[0])

    if isinstance(result, Image.Image):
        return result.convert("RGB")

    raise RemoteCallError(f"Unexpected result type from Space: {type(result)}")


# ----------------------------
# Public API
# ----------------------------
def swap_faces(src_img: ImageLike, dest_img: ImageLike) -> Image.Image:
    client = _get_client()

    src_path = _to_temp_png_path(src_img)
    dest_path = _to_temp_png_path(dest_img)

    try:
        # IMPORTANT: keyword args + api_name
        # This prevents usage-info spam + ensures stable signature.
        result = client.predict(
            src_img=handle_file(src_path),
            dest_img=handle_file(dest_path),
            api_name=API_NAME,
        )
        return _normalize_result_to_pil(result)

    except Exception as e:
        raise RemoteCallError(
            f"Remote face swap call failed for Space '{SPACE_ID}' "
            f"with api_name '{API_NAME}'."
        ) from e

    finally:
        _cleanup_temp(src_path, src_img)
        _cleanup_temp(dest_path, dest_img)


if __name__ == "__main__":
    import sys as _sys

    if len(_sys.argv) != 3:
        print("Usage: python face_swap.py <source_img> <target_img>")
        raise SystemExit(1)

    out = swap_faces(_sys.argv[1], _sys.argv[2])
    out.save("output.jpg")
    print("Saved output.jpg")

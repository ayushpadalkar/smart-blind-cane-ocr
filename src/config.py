from pathlib import Path


# =========================================================
# BASE DIRECTORIES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# IMAGE / OUTPUT DIRECTORIES
# =========================================================

OUTPUT_DIR = BASE_DIR / "assets" / "output"

IMAGE_DIR = BASE_DIR / "assets" / "images"


# =========================================================
# OCR SETTINGS
# =========================================================

OCR_CONFIDENCE = 0.50

OCR_LANGUAGE = "en"

OCR_VERSION = "PP-OCRv5"


# =========================================================
# CAMERA SETTINGS
# =========================================================

CAMERA_INDEX = 0

FRAME_WIDTH = 640

FRAME_HEIGHT = 480


# =========================================================
# TTS SETTINGS
# =========================================================

VOICE_RATE = 170

VOICE_VOLUME = 1.0

VOICE_ID = 0


# =========================================================
# LOGGING
# =========================================================

LOG_DIR = BASE_DIR / "assets" / "logs"

LOG_LEVEL = "INFO"


# =========================================================
# CREATE REQUIRED DIRECTORIES
# =========================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

IMAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)
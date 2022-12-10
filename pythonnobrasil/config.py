from pathlib import Path

from decouple import config

BASE_DIR = Path().parent / "pythonnobrasil"

GOOGLE_API_AUTH = config("GOOGLE_API_AUTH", default="google_auth.json")
GOOGLE_API_CALENDAR_ID = config("GOOGLE_API_CALENDAR_ID")

CONFERENCIAS_PATH = BASE_DIR.parent / "conferencias.toml"

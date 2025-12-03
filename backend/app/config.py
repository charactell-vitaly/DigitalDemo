import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory = backend folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Storage dirs
STORAGE_DIR = BASE_DIR / "storage"
INCOMING_ROOT = STORAGE_DIR / "incoming"
RESULTS_ROOT = STORAGE_DIR / "results"

# SQLite database file
DB_PATH = STORAGE_DIR / "documents.db"

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8808"))
API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Ensure required folders exist
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
INCOMING_ROOT.mkdir(parents=True, exist_ok=True)
RESULTS_ROOT.mkdir(parents=True, exist_ok=True)


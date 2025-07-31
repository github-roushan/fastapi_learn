from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent

load_dotenv(dotenv_path=f"{BASE_DIR}/.env")

POSTGRES_PASS = os.getenv('POSTGRES_PASS')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_DB = os.getenv('POSTGRES_DB')

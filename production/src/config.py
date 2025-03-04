# config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
EXTERNAL_API = os.getenv("EXTERNAL_API")

if not API_TOKEN or not EXTERNAL_API:
    raise ValueError("API_TOKEN o EXTERNAL_API no configurados en las variables de entorno")

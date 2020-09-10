# settings.py
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPEN_SKY_API_USER = os.environ.get("OPEN_SKY_API_USER")
OPEN_SKY_API_PW = os.environ.get("OPEN_SKY_API_PW")
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../backend"))

from dotenv import load_dotenv
load_dotenv()

from app import create_app

app = create_app()

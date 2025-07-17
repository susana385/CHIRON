# supabase_client.py
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv("supabase.env")
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(URL, KEY)

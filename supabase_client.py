# supabase_client.py
import os
from supabase import create_client

URL = "https://izmbnzpgpzwrjoxldokw.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml6bWJuenBncHp3cmpveGxkb2t3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3NjI5MzUsImV4cCI6MjA2NjMzODkzNX0.6VpEOTi9LGsENmJ9M-uRBQBEu0RaH2hp4Va_-MMCDCo"
supabase = create_client(URL, KEY)

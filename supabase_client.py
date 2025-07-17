import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv("supabase.env")
URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

@st.cache_resource
def get_supabase_client():
    return create_client(URL, KEY)

supabase = get_supabase_client()

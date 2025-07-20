# supabase_client.py
# supabase_client.py
import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega variáveis de ambiente (ajusta o nome se diferente)
load_dotenv("supabase.env")

@st.cache_resource
def get_supabase() -> Client:
    """
    Cria e cacheia uma única instância do cliente Supabase.
    Lança RuntimeError se faltar configuração.
    """
    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

    if not url:
        raise RuntimeError("SUPABASE_URL não definido em st.secrets ou ambiente.")
    if not key:
        raise RuntimeError("SUPABASE_KEY não definido em st.secrets ou ambiente.")

    return create_client(url, key)

# Tentativa de criação com captura de erro para feedback imediato no UI
try:
    supabase: Client = get_supabase()
    auth = supabase.auth
except Exception as e:
    # Mostra um erro visível no Streamlit (uma vez)
    st.error(f"❌ Falha ao inicializar cliente Supabase: {e}")
    # Opcional: re-levantar para parar a app, se preferires
    raise

supabase = get_supabase()
auth = supabase.auth

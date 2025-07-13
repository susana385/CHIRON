# Home.py
import streamlit as st
import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os
import base64


load_dotenv(dotenv_path="supabase.env")
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
#auth = supabase.auth
supabase = create_client(url,key,)

def show_logos(logo_paths_with_widths):
    logos_html = ""
    for path, width in logo_paths_with_widths:
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
            logos_html += f"<img src='data:image/png;base64,{encoded}' width='{width}' style='margin: 0 20px;'/>"

    st.markdown(
        f"""
        <div style='text-align: center; margin-bottom: 20px;'>
            {logos_html}
        </div>
        """,
        unsafe_allow_html=True
    )

# Must be first Streamlit command in your app
st.set_page_config(page_title="CHIRON System", layout="wide")
st.markdown(
    """
    <style>
      [data-testid="stSidebarNav"] {
        display: none;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

show_logos([
    ("Logo_CHIRON.png", 90),
    ("IDEAS_LAB.png",    180),
    ("Novologofct2021.png", 150),
])

st.title("Welcome to CHIRON System")
st.write("This system lets you **participate**, **supervise**, **manage**, or **administer** CHIRON simulations.")

email       = st.text_input("Email")
password    = st.text_input("Password", type="password")
role_code   = st.text_input("Profile type code (1=admin, 2=supervisor, 3=manager, 1234=participant)")

col1, col2 = st.columns(2)
with col1:
    if st.button("Log In"):
        try:
            signin = supabase.auth.sign_in_with_password({"email": email, "password": password})
            profile = (supabase.from_("profiles")
                            .select("role")
                            .eq("id", signin.user.id)
                            .single()
                            .execute()
                            .data)
        except Exception as e:
            st.error(f"Sign-in failed: {e}")
        else:
            # save session
            st.session_state["access_token"]  = signin.session.access_token
            st.session_state["refresh_token"] = signin.session.refresh_token
            st.session_state["user"]          = signin.user
            st.session_state["user_role"]     = profile["role"]

            # go to Welcome page
            st.query_params["welcome"]
            st.rerun()

with col2:
    if st.button("Sign Up"):
        if not role_code.strip():
            st.error("❗ You must enter a profile type code.")
        else:
            code = int(role_code)
            role_map = {1:"administrator", 2:"supervisor", 3:"manager", 1234:"participant"}
            if code not in role_map:
                st.error("Invalid code.")
            else:
                try:
                    auth_res = supabase.auth.sign_up({"email": email, "password": password})
                    supabase.from_("profiles").insert({
                        "id":               auth_res.user.id,
                        "username":         email,
                        "role":             role_map[code],
                        "profile_type_code": code
                    }).execute()
                    st.success("✅ Registered! Please confirm your email, then log in.")
                except Exception as e:
                    st.error(f"Sign-up error: {e}")

import streamlit as st

st.title("Sign in")

st.write("Prototype login: toggles a session flag only.")

email = st.text_input("Email")
pw = st.text_input("Password", type="password")

c1, c2 = st.columns(2)
with c1:
    if st.button("Sign in", key="login_signin"):
        st.session_state.is_authenticated = True
        st.success("Signed in (prototype)")
with c2:
    if st.button("Sign out", key="login_signout"):
        st.session_state.is_authenticated = False
        st.info("Signed out")

from __future__ import annotations
import streamlit as st
st.set_page_config(layout='wide', page_title='Welcome · For You')
from pages.SeniorNav_welcome_base import render
render("self")

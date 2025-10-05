from __future__ import annotations
import streamlit as st
from pages.SeniorNav_welcome_base import render
st.set_page_config(layout="wide", page_title="Welcome · Someone Else")
render("proxy")

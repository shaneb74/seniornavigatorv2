import streamlit as st

def inject_theme() -> None:
    """Minimal theme injector to keep pages running."""
    st.markdown(
        """
        <style>
          :root{
            --brand:#0B5CD8;
            --paper:#ffffff;
            --surface:#f6f8fa;
            --ink:#111418;
            --ink-muted:#6b7280;
          }
          .block-container{max-width:1160px;padding-top:8px;}
          header[data-testid="stHeader"]{background:transparent;}
          footer{visibility:hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

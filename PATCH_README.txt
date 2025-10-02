This patch updates app.py to:
- Register all pages referenced from Welcome and Hub (including gcp.py)
- Monkey‑patch st.switch_page globally with a safe wrapper that:
  * Forces targets to 'pages/*'
  * Verifies file existence
  * Falls back to Hub when a page isn't registered yet
This avoids hard crashes like the one you saw in hub.py line 37.

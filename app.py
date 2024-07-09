import streamlit as st
import json

from openai import AzureOpenAI
from app import sidebar
from app import pages
from app import upload
from app import describe

with open("config.json", "r") as f:
    config = json.load(f)

# App title
pages.show_home()

# app sidebar
with st.sidebar:
    sidebar.show_sidebar()

# Initialize OpenAI client with API key
api_key = config["api_key"]

client = AzureOpenAI(
    azure_endpoint=config["endpoint"],
    api_version=config["api_version"],
    api_key=api_key,
)

tabs = st.tabs(["Describe", "Upload"])

# Describe how the app should be built
with tabs[0]:
    describe.show_describe(config, api_key, client)

# Upload mock-up image of an app
with tabs[1]:
    upload.show_upload(config, api_key, client)

st.divider()
footer_html = """
<div style='text-align: center;'>
<p>Made with ❤️ by <a href="https://github.com/robrita/Azure-AI-App-Builder">RobRita</a>
</p>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)

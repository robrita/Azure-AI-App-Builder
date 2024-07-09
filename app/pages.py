import streamlit as st


def show_home():
    st.set_page_config(
        page_title="Azure AI App Builder",
        page_icon="🚀",
        # initial_sidebar_state="collapsed",
    )
    st.logo(
        "https://azure.microsoft.com/svghandler/ai-studio/?width=600&height=315",
        link="https://ai.azure.com/",
    )
    st.title("🚀Azure AI App Builder")

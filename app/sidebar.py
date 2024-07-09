import json
import time
import streamlit as st

with open("config.json", "r") as f:
    config = json.load(f)


# display the sidebar
def show_sidebar():
    st.header("💡About this app")
    st.write(
        "Generate an AI app either by **describing** your app in detail or **uploading** a mock-up image."
    )

    st.subheader("⚙️Settings", anchor=False)
    # capture user input
    with st.form("user_input"):
        endpoint = st.text_input(
            "Azure OpenAI Endpoint:",
            placeholder="https://sample.openai.azure.com",
            value=config["endpoint"],
            type="password",
        )
        api_key = st.text_input(
            "Azure OpenAI API Key:",
            placeholder="8cb78***************",
            value=config["api_key"],
            type="password",
        )
        api_version = st.text_input(
            "Azure OpenAI API Version:",
            placeholder="2024-02-15-preview",
            value=config["api_version"],
        )
        model = st.text_input(
            "Azure OpenAI Model Name:",
            placeholder="gpt-4o",
            value=config["model"],
        )

        submitted = st.form_submit_button("Update!")

    # update the config file
    if submitted:
        config["endpoint"] = endpoint
        config["api_key"] = api_key
        config["api_version"] = api_version
        config["model"] = model

        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)

        st.success("Settings updated successfully!")
        time.sleep(1)
        st.rerun()

    st.subheader("🛠Technology Stack", anchor=False)
    st.write("Python, Streamlit, Azure OpenAI, Azure AI")

    st.subheader("🏆Microsoft Global Hackathon 2024", anchor=False)
    st.write(
        "AI App Builder is proudly presented as Rob's innovative entry for the Microsoft Global Hackathon 2024."
    )

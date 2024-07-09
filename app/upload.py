import base64
import time
import json
import os
import streamlit as st

from tempfile import NamedTemporaryFile
from streamlit_image_select import image_select
from mockup_code import mockup_1, mockup_2


def show_upload(config: dict, api_key: str, client: object):
    upload_img = st.toggle("Upload your own mock-up images")
    if upload_img:
        st.subheader("Upload your own mock-up image")
        image_upload = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

        # Function to encode the image
        def encode_image(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")

        if image_upload:
            st.image(image_upload, use_column_width=True)

            # base64_image = encode_image(image_upload)
            # st.write(base64_image)

            bytes_data = image_upload.read()
            with NamedTemporaryFile(delete=False) as tmp:
                tmp.write(bytes_data)

    # Example images
    example_img = st.toggle("Try example mock-up images")
    if example_img:
        st.subheader("Try these example mock-up images")
        img = image_select(
            label="Select a mock-up image",
            images=["img/streamlit-app-mockup-1.png", "img/streamlit-app-mockup-2.png"],
        )

    with st.expander("System Prompt:"):
        with st.form("prompt_upload"):
            prompt = st.text_area(
                "⚙️",
                value=config["prompt_upload"],
                height=200,
            )

            submitted = st.form_submit_button("Update!")

        # update the config file
        if submitted:
            config["prompt_upload"] = prompt

            with open("config.json", "w") as f:
                json.dump(config, f, indent=2)

            st.success("Settings updated successfully!")
            time.sleep(1)
            st.rerun()

    # Start LLM process
    start_button = st.button(
        "Build", key="button_image_start", disabled=not (upload_img or example_img)
    )

    if any([upload_img, example_img]) == True:

        if "img" in locals() or "img" in globals():
            if start_button:
                with st.spinner("Processing ..."):
                    time.sleep(1.5)

                    if img == "img/streamlit-app-mockup-1.png":
                        st.subheader("Input")
                        st.image("img/streamlit-app-mockup-1.png")
                        st.subheader("Output")
                        mockup_1()

                    if img == "img/streamlit-app-mockup-2.png":
                        st.subheader("Input")
                        st.image("img/streamlit-app-mockup-2.png")
                        st.subheader("Output")
                        mockup_2()

        elif image_upload is not None and api_key and start_button:
            # if image_upload is not None and openai.api_key and start_button:
            with st.spinner("Processing ..."):
                base64_image = encode_image(tmp.name)

                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": config["prompt_upload"]},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                },
                            },
                        ],
                    }
                ]

                try:
                    # Response generation
                    full_response = ""
                    message_placeholder = st.empty()

                    for completion in client.chat.completions.create(
                        model=config["model"],
                        messages=messages,
                        max_tokens=1280,
                        stream=True,
                    ):

                        if (
                            completion.choices
                            and completion.choices[0].delta.content is not None
                        ):
                            full_response += completion.choices[0].delta.content
                            message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)

                    if "```python" in full_response:
                        parsed_output = (
                            full_response.split("```python")[1]
                            .lstrip("\n")
                            .split("```")[0]
                        )

                    # Clear results
                    if st.button("Clear", key="button_image_clear"):
                        os.remove(tmp.name)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

        else:
            if not image_upload and start_button:
                # if not image_upload and not img and start_button:
                st.warning("Please upload your mock-up image.")
            if not api_key:
                st.warning("Please provide your OpenAI API key.")

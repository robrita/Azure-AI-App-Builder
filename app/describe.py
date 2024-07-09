import json
import time
import os
import streamlit as st


def show_describe(config: dict, api_key: str, client: object, tmp_name: str = "tmp"):
    text_prompt = st.text_area(
        "Describe details on the functionalities of the Streamlit app that you want to build.",
        "",
        height=200,
    )

    with st.expander("System Prompt:"):
        with st.form("prompt_describe"):
            prompt = st.text_area(
                "⚙️",
                value=config["prompt_describe"],
                height=200,
            )

            submitted = st.form_submit_button("Update!")

        # update the config file
        if submitted:
            config["prompt_describe"] = prompt

            with open("config.json", "w") as f:
                json.dump(config, f, indent=2)

            st.success("Settings updated successfully!")
            time.sleep(1)
            st.rerun()

    # Start LLM process
    start_button = st.button(
        "Build", key="button_text_start", disabled=text_prompt == ""
    )

    if text_prompt != "" and api_key and start_button:
        with st.spinner("Processing ..."):
            messages = [
                {
                    "role": "system",
                    "content": config["prompt_describe"],
                },
                {"role": "user", "content": text_prompt},
            ]
        try:
            # Response generation
            full_response = ""
            message_placeholder = st.empty()

            for completion in client.chat.completions.create(
                model=config["model"],
                messages=messages,
                temperature=0.7,
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
                    full_response.split("```python")[1].lstrip("\n").split("```")[0]
                )
                # write to output file
                with open("output.py", "w") as file:
                    file.write(parsed_output)
                    st.write(
                        "Run the following command in your current working directory:"
                    )
                    st.success(f"streamlit run output.py")

            # Clear results
            if st.button(":orange[Clear]", key="button_text_clear"):
                os.remove(tmp_name)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    else:
        if not text_prompt and start_button:
            st.warning("Please provide your text prompt.")
        if not api_key:
            st.warning("Please provide your OpenAI API key.")

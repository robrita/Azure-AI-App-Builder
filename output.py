import streamlit as st
from streamlit_chat import message

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

st.title("Messenger Style Chat Application")

# User input
user_input = st.text_input("Type your message...", key="input")

if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append({"is_user": True, "text": user_input})
        # Here you can add the bot's response logic
        bot_response = "This is a response from the bot!"
        st.session_state.chat_history.append({"is_user": False, "text": bot_response})
        st.session_state.input = ""

# Display chat history
for chat in st.session_state.chat_history:
    message(chat['text'], is_user=chat['is_user'])

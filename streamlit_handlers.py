import streamlit as st
from dotenv import load_dotenv
import os

# This must be the first streamlit command called, otherwise it won't work
st.set_page_config(page_title="ChatGPT Clone", page_icon="💬")


def render_conversation():
    for message in st.session_state["chat_history"][1:]:
        if message["content"] is not None:
            with st.chat_message(
                name=message["role"],
                avatar="icons/database.png" if message["role"] == "function" else None,
            ):
                st.markdown(message["content"])


def render_qa_agent():
    if st.session_state.get("agent") is not None:
        with st.expander("📚 QA Agent"):
            for index, tool in enumerate(st.session_state["agent"].tools):
                st.write(f"**Tool name**: {tool.name}")
                st.write(f"**Tool description**: {tool.description}")
                if index != len(st.session_state["agent"].tools) - 1:
                    st.divider()


@st.cache_resource
def init():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY not found")
        exit(1)
    else:
        print("OPENAI_API_KEY found")


init()

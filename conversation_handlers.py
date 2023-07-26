import json
import os

import openai
import streamlit as st
from tenacity import retry, stop_after_attempt, wait_random_exponential

openai.api_key = os.getenv("OPENAI_API_KEY")
GPT_MODEL = st.secrets["llm"]["conversation_model"]


@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(
    messages, functions=None, function_call=None, model=GPT_MODEL
):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=functions if functions is not None else [],
            function_call=function_call if function_call is not None else "auto",
            stream=True,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def respond_franchise_inquiry(inquiry, st_callback=None):
    agent = st.session_state["agent"]
    return agent.run(inquiry, callbacks=[st_callback])


def execute_function_call(message, st_callback=None):
    if message["function_call"]["name"] == "respond_franchise_inquiry":
        inquiry = json.loads(message["function_call"]["arguments"])["inquiry"]
        results = respond_franchise_inquiry(inquiry=inquiry, st_callback=st_callback)
    else:
        results = f"Error: function {message['function_call']['name']} does not exist"
    return results

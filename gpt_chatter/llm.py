import json

import streamlit as st
from openai import APITimeoutError, AsyncOpenAI, RateLimitError

client = AsyncOpenAI(
    api_key=st.secrets["OPENAI_API_KEY"], base_url=st.secrets["OPENAI_BASE_URL"]
)


async def get_completion(messages, model="gpt-4o"):
    try:
        completion = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        response = completion.choices[0].message.content
    except Exception as e:
        raise Exception(e)

    return response

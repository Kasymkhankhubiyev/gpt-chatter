import asyncio

import streamlit as st
from openai import AsyncOpenAI, OpenAI

# from .agent import Agent


async def run():
    st.title("GPT-Like Bot")

    # client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    refresh_chat = st.sidebar.button("Refresh Chat")

    if refresh_chat:
        st.session_state.messages = []

    # client = Agent(st.session_state.messages)
    client = AsyncOpenAI(
        api_key=st.secrets["OPENAI_API_KEY"], base_url=st.secrets["OPENAI_BASE_URL"]
    )

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            completion = await client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            response = st.markdown(completion.choices[0].message.content)
        st.session_state.messages.append(
            {"role": "assistant", "content": completion.choices[0].message.content}
        )


if __name__ == "__main__":
    asyncio.run(run())

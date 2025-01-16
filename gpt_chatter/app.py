import asyncio
import json
import os
from typing import List

import streamlit as st
from openai import AsyncOpenAI, OpenAI

from gpt_chatter.agent import Agent, gen_titles


async def add_title_to_history(chats):
    with open(os.path.join("gpt_chatter", "serialized", "chats.json"), "w") as file:
        json.dump(chats, file)


async def get_available_chats() -> List[str]:
    chats = []
    if os.path.exists(os.path.join("gpt_chatter", "serialized", "chats.json")):
        with open(os.path.join("gpt_chatter", "serialized", "chats.json"), "r") as file:
            chats = json.load(file)
    return chats


async def run():

    TITLE = "New chat"
    CHATS = []

    st.title("GPT-Like Bot")

    agent = Agent(title=TITLE)

    refresh_chat = st.sidebar.button("Refresh Chat")

    if refresh_chat:
        st.session_state.messages = []
        agent.messages = []
        agent._serialize()

    chats_available = await get_available_chats()
    if chats_available:
        for chat in chats_available:
            if st.sidebar.button(chat):
                TITLE = chat
                agent = Agent(chat)
                # st.sidebar.write(f"Loaded session: {name}")
                st.title(chat)

            if "messages" not in st.session_state:
                st.session_state.messages = agent.messages

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    if "messages" not in st.session_state:
        st.session_state.messages = agent.messages

    # client = Agent(st.session_state.messages)

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        if agent.title == "New chat":
            new_title = await gen_titles(CHATS, message=prompt)
            TITLE = new_title
            agent = Agent(TITLE)
            chats_available.append(TITLE)
            await add_title_to_history(chats_available)
            st.title(TITLE)

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            completion = await agent(prompt)
            _response = st.markdown(completion)
        st.session_state.messages.append({"role": "assistant", "content": completion})


if __name__ == "__main__":
    asyncio.run(run())

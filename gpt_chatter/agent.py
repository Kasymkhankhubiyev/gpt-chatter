import json
import os

from .llm import get_completion


class Agent:
    def __init__(self, messages=[]):
        self.messages = messages

    async def __call__(self, user_message):
        self._check_for_retrieval(user_message)

        if user_message is not None:
            self.messages.append({"role": "user", "content": user_message})

        completion = await get_completion(self.messages, self.schema)
        self.messages.append({"role": "assistant", "content": completion.content})
        parsed_completion = completion.parsed

        return parsed_completion.message

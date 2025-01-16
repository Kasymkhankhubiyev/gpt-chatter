import json
import os

from .llm import get_completion

SAVE_DIR = os.path.join("gpt_chatter", "serialized")

if not os.path.exists(SAVE_DIR):
    os.mkdir(SAVE_DIR)


class Agent:
    def __init__(self, title: str, messages=[]):
        self.title = title

        if os.path.exists(os.path.join(SAVE_DIR, f"{title}.json")):
            with open(os.path.join(SAVE_DIR, f"{title}.json"), "r") as file:
                messages = json.load(file)

        self.messages = messages

    def _serialize(self):
        with open(os.path.join(SAVE_DIR, f"{self.title}.json"), "w") as file:
            json.dump(self.messages, file, ensure_ascii=False)

    def clear(self):
        self.messages = []
        if os.path.exists(os.path.join(SAVE_DIR, f"{self.title}.json")):
            os.remove(os.path.join(SAVE_DIR, f"{self.title}.json"))

    async def __call__(self, user_message):

        if user_message is not None:
            self.messages.append({"role": "user", "content": user_message})

        completion = await get_completion(self.messages)
        self.messages.append({"role": "assistant", "content": completion})
        self._serialize()

        return completion


async def gen_titles(titles, message):
    messages = [
        {
            "role": "user",
            "content": f"generate a short title for a chat based on user requet: {message}, the title must be unique, here is the list of already existing title: {titles}",
        }
    ]

    completion = await get_completion(messages, model="gpt-4o-mini")
    return completion

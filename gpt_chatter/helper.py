from .llm import get_completion


async def gen_titles(titles, message):
    messages = [
        {
            "role": "user",
            "content": f"generate a short title for a chat based on user requet: {message}, the title must be unique, here is the list of already existing title: {titles}",
        }
    ]

    completion = await get_completion(messages, model="gpt-4o-mini")
    return completion

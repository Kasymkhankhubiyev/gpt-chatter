import json

from openai import APITimeoutError, AsyncOpenAI, RateLimitError

client = AsyncOpenAI()


async def get_completion(messages):
    try:
        completion = await client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=messages,
        )

        response = completion.choices[0].message
    except Exception as e:
        raise Exception(e)

    return response

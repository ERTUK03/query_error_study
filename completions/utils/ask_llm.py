import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="http://localhost:8080/v1",
    api_key="dummy"
)

sem = asyncio.Semaphore(64)

async def ask_llm(prompt):
    async with sem:
        resp = await client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
        )

        return resp.choices[0].message.content
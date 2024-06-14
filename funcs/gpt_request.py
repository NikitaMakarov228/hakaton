import g4f, asyncio


async def gptReq(prompt: str) -> str:
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.FreeGpt,
            messages=[{"role": "user", "content": prompt}],
            provider=g4f.Provider.FreeGpt,
        )
        return response
    except Exception as e:
        print(e)
        return "error"

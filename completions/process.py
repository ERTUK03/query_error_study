import asyncio

async def process(dataset, name, process_fn):
    print(f"Current: {name}")
    tasks = [process_fn(i, ex) for i, ex in enumerate(dataset)]
    results = []
    for coro in asyncio.as_completed(tasks):
        result = await coro
        results.append(result)
        if len(results) % 100 == 0:
            print(f"Done {len(results)}/{len(dataset)}")
    return results
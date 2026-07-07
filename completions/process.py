import asyncio

async def process(dataset, name, process_fn, workers=64):
    print(f"Current: {name}")

    queue = asyncio.Queue()
    results = []

    for i, ex in enumerate(dataset):
        queue.put_nowait((i, ex))

    async def worker():
        while True:
            try:
                i, ex = queue.get_nowait()
            except asyncio.QueueEmpty:
                break

            try:
                result = await process_fn(i, ex)
                results.append(result)

                if len(results) % 100 == 0:
                    print(f"Done {len(results)}/{len(dataset)}")

            finally:
                queue.task_done()

    tasks = [
        asyncio.create_task(worker())
        for _ in range(workers)
    ]

    await asyncio.gather(*tasks)

    return results
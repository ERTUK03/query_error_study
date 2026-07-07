from .utils.ask_llm import ask_llm

async def complete(i, example):
    query = example["query"]
    answer = example["answer"]
    pred = await ask_llm(query)
    return {
        "id": i,
        "query": query,
        "prediction": pred,
        "ground_truth": answer
    }
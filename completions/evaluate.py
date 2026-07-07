from .utils.ask_llm import ask_llm
import json

def build_judge_prompt(query, ground_truth, prediction):
    return f"""
You are an evaluation system.

Task: Decide whether the prediction correctly answers the query, given the ground truth as the reference answer.

Step-by-step process (do this internally before answering):
1. Identify what the query is actually asking for.
2. From the ground truth, extract only the information that is relevant to answering that specific query. Call this the "required info."
3. Check whether the prediction contains the required info, in any wording.
4. Ignore any ground truth details that are not necessary to answer the query — do not penalize the prediction for omitting them.
5. Check whether the prediction contradicts the required info. Contradiction = incorrect, regardless of anything else.
6. Extra information in the prediction is fine as long as it doesn't contradict the required info.

Rules:
- Correct = prediction conveys the same required info as ground truth, in meaning (wording can differ).
- Missing required info (i.e., info necessary to answer the query) = incorrect.
- Missing info from the ground truth that is NOT necessary to answer the query = still correct.
- Any contradiction of the required info = incorrect.

Return ONLY valid JSON:
{{
    "label": "correct" or "incorrect",
    "confidence": 0-100,
    "reason": "one short sentence"
}}

Query:
{query}

Ground truth:
{ground_truth}

Prediction:
{prediction}
""".strip()

async def evaluate(i, example):
    MAX_RETRIES = 3
    
    query = example["query"]
    ground_truth = example["ground_truth"]
    prediction = example["prediction"]

    prompt = build_judge_prompt(query, ground_truth, prediction)

    last_raw = None

    for attempt in range(MAX_RETRIES):
        raw = await ask_llm(prompt)
        last_raw = raw

        try:
            parsed = json.loads(raw)
            break
        except Exception:
            continue
    else:
        return {
            "id": i,
            "query": query,
            "ground_truth": ground_truth,
            "prediction": prediction,
            "judge_label": None,
            "confidence": None,
            "reason": None,
            "needs_review": True,
            "json_failed": True,
            "raw_judge": last_raw
        }

    confidence = parsed.get("confidence")

    needs_review = (
        confidence is None or
        not isinstance(confidence, (int, float)) or
        confidence < 90
    )

    return {
        "id": i,
        "query": query,
        "ground_truth": ground_truth,
        "prediction": prediction,
        "judge_label": parsed.get("label"),
        "confidence": confidence,
        "reason": parsed.get("reason"),
        "needs_review": needs_review,
        "json_failed": False,
        "raw_judge": last_raw
    }
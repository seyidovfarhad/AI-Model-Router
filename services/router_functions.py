from fastapi import HTTPException, status
import numpy as np
import httpx
from services.retry import chat_with_retry
from settings.settings import questions, faq_doc, system_prompt

# keyword match
def get_answer_by_memory(question):
    question = question.lower().replace(" ", "")
    for p in faq_doc:
        if p in question and len(question) <= faq_doc[p][0]:
            return faq_doc[p][1]
    return None


# vector similarity search
def search_similar(question, model, embeddings):
    question = model.encode(question, convert_to_tensor=True)
    similarities = model.similarity(embeddings, question).tolist()
    if np.max(similarities) > 0.65:
        best_idx = np.argmax(similarities)
        for i, v in enumerate(questions):
            if i == best_idx:
                return questions[v]
    return None

# LLM
async def generate_text(question:str, client:httpx.AsyncClient, attempt:int = 3, base_delay:int = 3):
    payload = {"model": "openrouter/free",
            "messages": [{"role": "system", "content": system_prompt},
                         {"role": "user", "content": question}]}
    try:
        result = await chat_with_retry(attempt, base_delay, payload, client)
        return result
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"OpenRouter API error ({e.response.status_code}): {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Network error when accessing OpenRouter: {str(e)}")
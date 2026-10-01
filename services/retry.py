from fastapi import status
from settings.settings import RETRYABLE_STATUS_CODES, OPENROUTER_URL
import httpx
import asyncio



def get_retry_delay(response: httpx.Response, attempt: int, base_delay: float) -> float:
    """Determines the optimal wait time based on the status code and headers.."""
    status_code = response.status_code

    # 1. If it's a 429 error, look for the `Retry-After` header from OpenRouter.
    if status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                delay = float(retry_after)
                return delay
            except ValueError:
                pass  # If the value is not a number (e.g., a date), we fall back to the basic logic.
        return max(base_delay * (2 ** (attempt - 1)), 2.0)  # For the 429, it's better to take a slightly longer pause.

    # 2. If it's a 408 (Request Timeout)—meaning the server simply dropped the connection—we retry quickly.
    if status_code == status.HTTP_408_REQUEST_TIMEOUT:
        return 0.5

    # 3. For 502, 503, and 504 — classic exponential backoff.
    return base_delay * (2 ** (attempt - 1))


async def chat_with_retry(attempt, base_delay, payload, client):
    try:
        while attempt > 0:
            response = await client.post(OPENROUTER_URL, json=payload)
            if response.status_code in RETRYABLE_STATUS_CODES:
                delay = get_retry_delay(response, attempt, base_delay)
                await asyncio.sleep(delay)
            else:
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]

            attempt -= 1
    except:
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
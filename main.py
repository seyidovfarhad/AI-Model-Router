from fastapi import FastAPI, Depends
from sentence_transformers import SentenceTransformer
from contextlib import asynccontextmanager
import httpx
from settings.settings import questions
from dependencies import get_router, get_client, get_embedding_model, get_embedding, get_exec_times
import time
import os
import uvicorn
from dotenv import load_dotenv
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
@asynccontextmanager
async def lifespan(app:FastAPI):
    app.state.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    app.state.embedding = app.state.embedding_model.encode(list(questions.keys()), convert_to_tensor=True)
    app.state.client = app.state.httpx_client = httpx.AsyncClient(
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"})
    app.state.optimal_exec_time = []
    app.state.non_optimal_exec_time = []
    yield
    await app.state.httpx_client.aclose()


app = FastAPI(lifespan=lifespan)

@app.post("/chat")
async def generate(question:str,
                   optimal:bool=True,
                   router=Depends(get_router),
                   client=Depends(get_client),
                   embedding_model=Depends(get_embedding_model),
                   embeddings=Depends(get_embedding),
                   exec_times = Depends(get_exec_times)
                   ):
    optimal_exec_time, non_optimal_exec_time = exec_times
    if optimal:
        start_time = time.perf_counter()
        result = await router.route(question, client, embedding_model, embeddings, optimal)
        optimal_result_time = time.perf_counter() - start_time
        optimal_exec_time.append(round(optimal_result_time,5))

        start_time = time.perf_counter()
        _ = await router.route(question, client, embedding_model, embeddings, optimal=False)
        non_optimal_result_time = time.perf_counter() - start_time
        non_optimal_exec_time.append(round(non_optimal_result_time,5))

    if not optimal:
        start_time = time.perf_counter()
        result = await router.route(question, client, embedding_model, embeddings, optimal=False)
        result_time = time.perf_counter() - start_time
        optimal_exec_time.append(round(result_time, 5))
        non_optimal_exec_time.append(round(result_time, 5))

    return result
@app.post("/getComparisonStat")
async def get_statistics(exec_time_difference = Depends(get_exec_times)):
    optimal_times, non_optimal_times = exec_time_difference
    return {
        "optimal_exec_time": optimal_times,
        "non_optimal_exec_time": non_optimal_times
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
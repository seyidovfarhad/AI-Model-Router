import asyncio
from services.router_functions import get_answer_by_memory, search_similar, generate_text

# router
class Router:
    async def process_request_optimal_way(self, question, client, embedding_model, embeddings):
        result = await asyncio.to_thread(get_answer_by_memory, question)
        if result:
            return result
        result = await asyncio.to_thread(search_similar, question, embedding_model, embeddings)
        if result:
            return result
        return await generate_text(question, client)

    async def direct_process_request(self, question, client):
        return await generate_text(question, client)

    async def route(self, question, client, embedding_model, embeddings, optimal):
        if optimal:
            return await self.process_request_optimal_way(question, client, embedding_model, embeddings)
        else:
            return await self.direct_process_request(question, client)
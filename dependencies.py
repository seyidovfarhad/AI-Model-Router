from fastapi import Request
from services.routing import Router

def get_embedding_model(request:Request):
    return request.app.state.embedding_model

def get_embedding(request:Request):
    return request.app.state.embedding

def get_client(request:Request):
    return request.app.state.client

def get_exec_times(request:Request):
    return request.app.state.optimal_exec_time, request.app.state.non_optimal_exec_time

def get_router() -> Router:
    return Router()
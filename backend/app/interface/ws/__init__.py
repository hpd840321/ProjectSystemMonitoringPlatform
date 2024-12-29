from fastapi import APIRouter, Depends
from .agent import agent_websocket_endpoint
from ..api.v1.dependencies import get_agent_service

ws_router = APIRouter()

ws_router.websocket("/ws/agents/{agent_id}")(agent_websocket_endpoint) 